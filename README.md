# ICAP Stub Server

ICAP Stub Server — тестовый ICAP‑сервер для проверки интеграций и сценариев обработки ICAP. Сервер принимает входящие ICAP‑запросы на нескольких портах и возвращает ответы по заранее заданным параметрам. Настройки задаются через `config.ini`, что позволяет быстро моделировать разные варианты поведения без правок кода.

## Назначение
- Эмуляция ICAP‑сервисов для систем DLP/AV/Proxy.
- Быстрая проверка клиентских интеграций (REQMOD/RESPMOD/OPTIONS).
- Тестирование таймаутов и кодов ответа на разных портах.

## Требования
- Python 3.12
- Docker (опционально)

## Установка
Создать виртуальное окружение и установить зависимости для разработки:
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

## Запуск локально
```bash
python -m app.main
```

## Конфигурация
Поведение сервера задается через `config.ini`.

### Секция `[server]`
- `host` — IP‑адрес прослушивания. Пример: `0.0.0.0`
- `log_level` — уровень логирования. Пример: `INFO`, `DEBUG`
- `default_response_code` — код ответа, если сервис не найден или метод не разрешен
- `default_response_delay_ms` — задержка (мс) для ответа по умолчанию

### Секция сервиса `[service:<name>]`
Каждый сервис задается отдельным блоком и привязан к порту:
- `port` — порт, на котором обслуживается сервис
- `reqmod` — разрешить обработку запросов REQMOD (`true`/`false`)
- `respmod` — разрешить обработку запросов RESPMOD (`true`/`false`)
- `response_code` — ICAP‑код ответа
- `response_delay_ms` — задержка перед ответом в мс

### Пример
```ini
[server]
host = 0.0.0.0
log_level = INFO
default_response_code = 404
default_response_delay_ms = 0

[service:scan]
port = 1344
reqmod = true
respmod = false
response_code = 200
response_delay_ms = 0

[service:rewrite]
port = 1344
reqmod = false
respmod = true
response_code = 200
response_delay_ms = 10
```

## Docker
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
