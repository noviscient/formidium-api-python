# Formidium Python API

A python wrapper for Formidium API.

Notes:
Claude was using UV (https://docs.astral.sh/uv) to manage the environment.

You may need to install UV (in a terminal in your project):
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

You may need to enable the running of unsigned scripts-
    Start Windows PowerShell with the "Run as Administrator" option. Only members of the Administrators group on the computer can change the execution policy.
    Enable running unsigned scripts by entering:
    set-executionpolicy remotesigned

To install the virtual environment in .venv run "uv sync"
Activate the environment with source .venv/bin/activate   (cd ./.venv/Scripts .... ./activate.bat)
Follow the instructions in Readme to set up the .env file and test it.

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

```python -m pytest tests.py::test_trades
```
