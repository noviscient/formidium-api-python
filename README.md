# Formidium Python API

A python wrapper for Formidium API.

## Quick Start

```python
from formidium import API

api = API(
    base_url="https://base.url.com",
    api_key="my_key",
    passphrase="my_passphrase",
    api_secret="my_secret"
)

api.trades(...)

api.positions(...)
```

## Running Tests

### Prerequisites for test running

- Install `dev-dependencies` in `pyproject.toml`
- Create a `.env` file at the root folder
- Specify the values listed in `.env.example`

### Running the tests

Run all at once:

```python
pytest
```

Run a specific test:

```python
pytest tests.py::test_trades
```
