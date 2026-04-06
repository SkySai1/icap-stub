# Response Builder

## Purpose
Generate ICAP response bytes based on a response plan.

## Inputs
- `ResponsePlan` with status code and delay
- Optional extra ICAP headers (e.g., `Methods` for OPTIONS)

## Outputs
- ICAP response bytes

## Conditions and Logic
- Map status code to a short status text
- Include minimal ICAP headers
- Append optional extra headers before the blank line terminator

## Flow (Mermaid)
```mermaid
flowchart TD
    A[Start] --> B[Build status line]
    B --> C[Add headers]
    C --> D[Encode to bytes]
    D --> E[Return response]
```
