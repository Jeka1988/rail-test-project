"""Load test data from YAML and environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from enums.account import AccountName, AccountType, CredentialKey

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = ROOT_DIR / "config" / "test_data.yaml"


def load_test_data(path: Path | None = None) -> dict[str, Any]:
    """Load YAML test data and apply optional environment overrides."""
    load_dotenv(ROOT_DIR / ".env")
    data_path = path or DEFAULT_DATA_PATH

    with data_path.open(encoding="utf-8") as data_file:
        data: dict[str, Any] = yaml.safe_load(data_file)

    data["base_url"] = os.getenv("BASE_URL", data["base_url"])

    credentials = data["credentials"]
    credentials[CredentialKey.USERNAME.value] = os.getenv(
        "BANK_USERNAME",
        credentials[CredentialKey.USERNAME.value],
    )
    credentials[CredentialKey.PASSWORD.value] = os.getenv(
        "BANK_PASSWORD",
        credentials[CredentialKey.PASSWORD.value],
    )

    for account in data["accounts"]:
        account["name"] = AccountName(account["name"]).value
        account["type"] = AccountType(account["type"]).value

    transfer = data["transfer"]
    transfer["from_account"] = AccountName(transfer["from_account"]).value
    transfer["to_account"] = AccountName(transfer["to_account"]).value

    send_money = data["send_money"]
    send_money["from_account"] = AccountName(send_money["from_account"]).value

    bill_pay = data["bill_pay"]
    bill_pay["from_account"] = AccountName(bill_pay["from_account"]).value

    _override_amount(data["transfer"], "amount", "TRANSFER_AMOUNT")
    _override_amount(data["send_money"], "amount", "SEND_MONEY_AMOUNT")
    _override_amount(data["bill_pay"], "amount", "BILL_PAY_AMOUNT")

    return data


def _override_amount(section: dict[str, Any], key: str, env_name: str) -> None:
    if os.getenv(env_name):
        section[key] = float(os.environ[env_name])
