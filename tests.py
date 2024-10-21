import os
import datetime

import pytest

from formidium import Api


@pytest.fixture
def api():
    BASE_URL = os.environ["BASE_URL"]
    API_KEY = os.environ["API_KEY"]
    PASSPHRASE = os.environ["PASSPHRASE"]
    API_SECRET = os.environ["API_SECRET"]

    return Api(
        base_url=BASE_URL,
        api_key=API_KEY,
        passphrase=PASSPHRASE,
        api_secret=API_SECRET,
    )


def test_portfolio_extract(api: Api):
    resp = api.portfolio_extract(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )

    assert resp.status_code == 200


def test_investor_allocation(api: Api):
    resp = api.investor_allocation(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
        investor_number="SSLPINV115",
    )

    assert resp.status_code == 200


def test_trades(api: Api):
    resp = api.trades(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )
    assert resp.status_code == 200


def test_positions(api: Api):
    resp = api.positions(
        fund_names=["CY Oliverware FUND"],
        date=datetime.date(2022, 1, 1),
    )
    assert resp.status_code == 200


def test_performance(api: Api):
    resp = api.performance(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )
    assert resp.status_code == 200


def test_balance_sheet(api: Api):
    resp = api.balance_sheet(
        fund_names=["CY Oliverware FUND"],
        end_date=datetime.date(2022, 1, 31),
    )
    assert resp.status_code == 200


def test_income_statement(api: Api):
    resp = api.income_statement(
        fund_names=["CY Oliverware FUND"],
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )
    assert resp.status_code == 200


def test_ledger_accounts(api: Api):
    resp = api.ledger_accounts(
        fund_name="CY Oliverware FUND",
    )
    assert resp.status_code == 200


def test_custodian_accounts(api: Api):
    resp = api.custodian_accounts(
        fund_name="CY Oliverware FUND",
    )
    assert resp.status_code == 200


def test_ledger_account_detail(api: Api):
    resp = api.ledger_account_detail(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
        broker_account_numbers=["CY01", "Other"],
        gl_accounts=[
            "Capital Addition",
            "Investment In Cryptocurrencies, (At Cost)",
            "Performance Fees Payable",
            "Miscellaneous Income",
        ],
    )
    assert resp.status_code == 200


def test_fx_rates(api: Api):
    resp = api.fx_rates(
        destination_currency="GBP",
        start_date=datetime.date(2021, 11, 30),
        end_date=datetime.date(2021, 12, 31),
    )
    assert resp.status_code == 200
