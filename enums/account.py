from __future__ import annotations

from enum import Enum


class CredentialKey(str, Enum):
    USERNAME = "username"
    PASSWORD = "password"


class ScenarioName(str, Enum):
    DEFAULT_ACCOUNT_LIFECYCLE = "default_account_lifecycle"
    INSUFFICIENT_FUNDS_TRANSFER = "insufficient_funds_transfer"


class LoginErrorMessage(str, Enum):
    INVALID_CREDENTIALS = "username or password you entered is incorrect"


class TransferErrorMessage(str, Enum):
    INSUFFICIENT_FUNDS = "Insufficient funds"


class PageName(str, Enum):
    LOGIN = "login"
    DASHBOARD = "dashboard"
    ACCOUNTS = "accounts"
    TRANSFER = "transfer"
    SEND_MONEY = "send_money"
    BILL_PAY = "bill_pay"
    TRANSACTIONS = "transactions"
