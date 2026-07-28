"""Shared enums for fixed domain values used by tests and page functions."""

from __future__ import annotations

from enum import Enum


class CredentialKey(str, Enum):
    USERNAME = "username"
    PASSWORD = "password"


class ScenarioName(str, Enum):
    DEFAULT_ACCOUNT_LIFECYCLE = "default_account_lifecycle"


class PageName(str, Enum):
    LOGIN = "login"
    DASHBOARD = "dashboard"
    ACCOUNTS = "accounts"
    TRANSFER = "transfer"
    SEND_MONEY = "send_money"
    BILL_PAY = "bill_pay"
    TRANSACTIONS = "transactions"
