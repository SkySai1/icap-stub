# ICAP Stub Server

ICAP Stub Server — тестовый ICAP-сервер для проверки интеграций и сценариев обработки ICAP.

## Требования
- Python 3.12
- Docker (опционально)

## Запуск локально
```bash
python -m app.main
```

## Конфигурация
Поведение сервера задается через `config.ini`.

Пример базовой конфигурации:
```ini
[server]
host = 0.0.0.0

[port:1344]
response_code = 200
response_delay_ms = 0
```

## Сборка и запуск в Docker
Сборка образа:
```bash
docker build -t icap-stub .
```

Запуск контейнера:
```bash
docker run --rm -p 1344:1344 -p 1345:1345 -v $(pwd)/config.ini:/app/config.ini:ro icap-stub
```

Запуск через Docker Compose:
```bash
docker compose up --build
```

## Тесты
```bash
pytest tests/
```

## Линтер и форматтер
```bash
ruff check .
ruff format .
```
