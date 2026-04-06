# Config Loader

## Purpose
Parse `config.ini` and return structured configuration objects for the server.

## Inputs
- Path to `config.ini`

## Outputs
- `ServerConfig` with host, log level, and per-port configuration

## Conditions and Logic
- Validate presence of `[server]` section
- Extract `host`
- Extract `log_level`
- Collect every `[port:<number>]` section
- Require at least one port definition

## Flow (Mermaid)
```mermaid
flowchart TD
    A[Start] --> B[Read INI file]
    B --> C{Has server}
    C -- No --> D[Error]
    C -- Yes --> E[Read host]
    E --> F[Collect port sections]
    F --> G{Any ports?}
    G -- No --> D
    G -- Yes --> H[Return ServerConfig]
```
