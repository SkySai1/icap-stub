# ICAP Server

## Purpose
Accept ICAP connections on multiple ports and send responses via handlers.

## Inputs
- List of `ListeningPort` definitions

## Outputs
- Network responses to connected clients

## Conditions and Logic
- Spawn one thread per listening port
- Accept connections in a loop
- Delegate response planning to port handlers
- For OPTIONS requests, include `Methods` header based on allowed methods
- When debug logging is enabled, log response decision details and raw response
- Send ICAP response and close connection

## Flow (Mermaid)
```mermaid
flowchart TD
    A[Start] --> B[Create threads per port]
    B --> C[Listen on port]
    C --> D[Accept connection]
    D --> E[Handle client]
    E --> F{OPTIONS?}
    F -- Yes --> G[Add Methods header]
    F -- No --> H[Build response]
    G --> H
    H --> I[Send response]
    I --> D
```
