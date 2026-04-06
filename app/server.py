"""Network server for accepting ICAP connections."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Thread
from typing import Iterable
import logging
import socket
import time

from app.handlers.port_handler import PortHandler
from app.protocol.icap import parse_request_line, read_request
from app.services.response_builder import ResponseBuilder


@dataclass(frozen=True)
class ListeningPort:
    """Definition of a port and its handler."""

    host: str
    handler: PortHandler


class IcapServer:
    """Accept ICAP connections on multiple ports."""

    def __init__(self, ports: Iterable[ListeningPort]) -> None:
        """Initialize server with a collection of ports."""

        self._ports = list(ports)
        self._threads: list[Thread] = []
        self._response_builder = ResponseBuilder()
        self._logger = logging.getLogger(self.__class__.__name__)

    def start(self) -> None:
        """Start listening on configured ports."""

        if self._logger.isEnabledFor(logging.DEBUG):
            for port in self._ports:
                for service_name, route in port.handler.services.items():
                    if route.reqmod:
                        self._logger.debug(
                            "Service ready on %s:%s method=REQMOD service=%s",
                            port.host,
                            port.handler.port,
                            service_name,
                        )
                    if route.respmod:
                        self._logger.debug(
                            "Service ready on %s:%s method=RESPMOD service=%s",
                            port.host,
                            port.handler.port,
                            service_name,
                        )

        for port in self._ports:
            thread = Thread(target=self._listen_on_port, args=(port,), daemon=True)
            thread.start()
            self._threads.append(thread)

        for thread in self._threads:
            thread.join()

    def _listen_on_port(self, port: ListeningPort) -> None:
        """Listen for incoming connections on a single port."""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((port.host, port.handler.port))
            server_socket.listen()
            self._logger.info("Listening on %s:%s", port.host, port.handler.port)

            while True:
                client_socket, _address = server_socket.accept()
                with client_socket:
                    self._handle_client(client_socket, port.handler)

    def _handle_client(self, client_socket: socket.socket, handler: PortHandler) -> None:
        """Handle a single client connection."""

        request_text = read_request(client_socket.recv(65535))
        method, service = parse_request_line(request_text)
        self._logger.debug(
            "Received request on port %s: %s %s",
            handler.port,
            method or "UNKNOWN",
            service or "-",
        )
        plan, requested_service, resolved_service = handler.plan_response(request_text)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(
                "Service requested on port %s: %s",
                handler.port,
                requested_service or "-",
            )
            self._logger.debug(
                "Request method on port %s: %s",
                handler.port,
                method or "UNKNOWN",
            )
            self._logger.debug(
                "Service resolved on port %s: %s",
                handler.port,
                resolved_service or "none",
            )
            self._logger.debug("Raw request on port %s:\n%s", handler.port, request_text)

        if plan.delay_ms:
            time.sleep(plan.delay_ms / 1000)

        response = self._response_builder.build(plan)
        client_socket.sendall(response)
