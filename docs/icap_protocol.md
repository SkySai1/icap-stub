# ICAP Protocol Helpers

## Purpose
Parse ICAP request lines to determine method and service name for routing.

## Inputs
- Raw ICAP request bytes

## Outputs
- Request text (decoded)
- Parsed method and service name

## Conditions and Logic
- Decode bytes with safe fallbacks
- Parse first line as `METHOD icap://host/service ICAP/1.0`
- Extract service name after the last `/`

## Flow (Mermaid)
```mermaid
flowchart TD
    A[Start] --> B[Decode request bytes]
    B --> C[Read first line]
    C --> D[Split into parts]
    D --> E[Extract method]
    D --> F[Extract service]
    E --> G[Return method/service]
    F --> G
```
