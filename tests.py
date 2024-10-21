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
    data = api.portfolio_extract(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 1),
    )
    assert data["pageCount"] > 0


def test_investor_allocation(api: Api):
    data = api.investor_allocation(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2021, 12, 31),
        end_date=datetime.date(2022, 1, 31),
        investor_number="CYOLIVERWAREINV01",
    )
    assert data["pageCount"] > 0


def test_trades(api: Api):
    data = api.trades(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )
    assert data["pageCount"] > 0


def test_positions(api: Api):
    data = api.positions(
        fund_names=["CY Oliverware FUND"],
        date=datetime.date(2022, 1, 1),
    )
    assert data["pageCount"] > 0


def test_performance(api: Api):
    data = api.performance(
        fund_name="CY Oliverware FUND",
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )
    assert data["pageCount"] > 0


def test_balance_sheet(api: Api):
    data = api.balance_sheet(
        fund_names=["CY Oliverware FUND"],
        end_date=datetime.date(2022, 1, 31),
    )
    # typo... what can we do
    assert "TotalNetAsets" in data


def test_income_statement(api: Api):
    data = api.income_statement(
        fund_names=["CY Oliverware FUND"],
        start_date=datetime.date(2022, 1, 1),
        end_date=datetime.date(2022, 1, 31),
    )

    assert "IncomesList" in data


def test_ledger_accounts(api: Api):
    data = api.ledger_accounts(
        fund_name="CY Oliverware FUND",
    )
    assert len(data["resultList"]) > 0


def test_custodian_accounts(api: Api):
    data = api.custodian_accounts(
        fund_name="CY Oliverware FUND",
    )
    assert len(data["resultList"]) > 0


def test_ledger_account_detail(api: Api):
    data = api.ledger_account_detail(
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
    assert len(data["resultList"]) > 0


def test_fx_rates(api: Api):
    data = api.fx_rates(
        destination_currency="GBP",
        start_date=datetime.date(2021, 11, 30),
        end_date=datetime.date(2021, 12, 31),
    )
    assert data["pageCount"] > 0
