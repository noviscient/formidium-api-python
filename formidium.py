import time
import base64
import datetime

import requests
from requests.models import Response
from tzlocal import get_localzone_name


class Api:
    def __init__(self, base_url: str, api_key: str, passphrase: str, api_secret: str):
        self.base_url = base_url
        self.api_key = api_key
        self.passphrase = passphrase
        self.api_secret = api_secret

        self._tz_name = get_localzone_name()

    @staticmethod
    def encrypt(
        api_key: str, api_secret: str, passphrase: str, current_time: str
    ) -> str:
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat import backends
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives import ciphers

        message = f"{current_time}{api_key}{passphrase}{api_secret}"
        key = api_secret.encode()
        salt = passphrase.encode()

        backend = backends.default_backend()

        # Derive a 32-byte encryption key from the provided key and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=65536,  # Adjust the number of iterations as needed for your use case
            backend=backend,
        )
        derived_key = kdf.derive(key)

        # Pad the message
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()

        # Generate a random 16-byte IV (Initialization Vector)
        iv = iv = bytes([0] * 16)

        # os.urandom(16) #{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }

        # Create the cipher using AES-256 in CBC mode
        cipher = ciphers.Cipher(
            ciphers.algorithms.AES(derived_key), ciphers.modes.CBC(iv), backend=backend
        )

        # Encrypt the data
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Return the derived key, IV, and ciphertext as bytes
        return base64.b64encode(ciphertext).decode()

    @property
    def header(self) -> dict:
        current_time = round(time.time() * 1000)

        signature = self.encrypt(
            self.api_key, self.api_secret, self.passphrase, str(current_time)
        )
        header = {
            "signature": signature,
            "x-api-key": self.api_key,
            "timeZone": self._tz_name,
            "timeStamp": str(current_time),
            "content-type": "application/json",
        }
        return header

    def _make_post_request(self, endpoint: str, data: dict) -> Response:
        base_url = self.base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        url = f"{base_url}{endpoint}"

        return requests.post(url, json=data, headers=self.header)

    def portfolio_extract(
        self, fund_name: str, start_date: datetime.date, end_date: datetime.date
    ) -> Response:
        """A portfolio extract of the fund over a date range."""

        ENDPOINT = "portfolioExtract"
        data = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundName": fund_name,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def investor_allocation(
        self,
        fund_name: str,
        start_date: datetime.date,
        end_date: datetime.date,
        investor_number: str,
    ) -> Response:
        """Investor allocation for a specific investor over a date range."""

        ENDPOINT = "investorAllocationAllFrequency"
        data = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundName": fund_name,
            "investorNumber": investor_number,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def trades(
        self, fund_name: str, start_date: datetime.date, end_date: datetime.date
    ) -> Response:
        """Trades for the fund over a date range."""

        ENDPOINT = "trades"
        data = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundName": fund_name,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def positions(self, fund_names: list[str], date: datetime.date) -> Response:
        """Positions for the fund on a specific date."""

        ENDPOINT = "positionData"
        data = {
            "date": date.strftime("%Y-%m-%d"),
            "fundList": fund_names,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def performance(
        self, fund_name: str, start_date: datetime.date, end_date: datetime.date
    ) -> Response:
        """Rate of return in multiple frequencies along with fees."""

        ENDPOINT = "performanceData"
        data = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundName": fund_name,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def balance_sheet(self, fund_names: list[str], end_date: datetime.date) -> Response:
        """Balance sheet for one or more funds."""

        ENDPOINT = "balanceSheet"
        data = {
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundList": fund_names,
            "page": 0,
        }
        return self._make_post_request(ENDPOINT, data)

    def income_statement(
        self, fund_names: list[str], start_date: datetime.date, end_date: datetime.date
    ) -> Response:
        """Income statement for one or more funds."""

        ENDPOINT = "incomeStatement"
        data = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundList": fund_names,
        }
        return self._make_post_request(ENDPOINT, data)

    def ledger_accounts(self, fund_name: str) -> Response:
        """Ledger accounts for the fund."""

        ENDPOINT = "ledgerAccount"
        data = {"fundName": fund_name}
        return self._make_post_request(ENDPOINT, data)

    def custodian_accounts(self, fund_name: str) -> Response:
        """Custodian accounts for the fund."""

        ENDPOINT = "custodianAccount"
        data = {"fundName": fund_name}
        return self._make_post_request(ENDPOINT, data)

    def ledger_account_detail(
        self,
        fund_name: str,
        broker_account_numbers: list[str],
        gl_accounts: list[str],
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> Response:
        """General ledger account details."""

        ENDPOINT = "generalLedgerWithCustodian"
        data = {
            "page": 0,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "fundName": fund_name,
            "brokerAccountList": broker_account_numbers,
            "nameOfGLAccountList": gl_accounts,
        }
        return self._make_post_request(ENDPOINT, data)

    def fx_rates(
        self,
        destination_currency: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> Response:
        """Exchange rates for USD to a specific currency over a date range."""

        ENDPOINT = "exchangeRateData"
        data = {
            "destinationCurrency": destination_currency,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
        }
        return self._make_post_request(ENDPOINT, data)
