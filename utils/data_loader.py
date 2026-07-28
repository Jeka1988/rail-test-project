"""Load test data from YAML and environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from enums.account import CredentialKey

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = ROOT_DIR / "config" / "test_data.yaml"


def load_test_data(path: Path | None = None) -> dict[str, Any]:
    """Load YAML test data and apply optional environment overrides."""
    load_dotenv(ROOT_DIR / ".env")
    data_path = _resolve_data_path(path)

    with data_path.open(encoding="utf-8") as data_file:
        data: dict[str, Any] = yaml.safe_load(data_file)

    _apply_overrides(data)
    return data


def _resolve_data_path(path: Path | None) -> Path:
    if path is not None:
        return path

    env_path = os.getenv("TEST_DATA_PATH")
    if not env_path:
        return DEFAULT_DATA_PATH

    candidate = Path(env_path)
    if not candidate.is_absolute():
        candidate = ROOT_DIR / candidate
    return candidate


def _apply_overrides(data: dict[str, Any]) -> None:
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

    invalid_credentials = data["invalid_credentials"]
    _override_str(invalid_credentials, CredentialKey.USERNAME.value, "BANK_INVALID_USERNAME")
    _override_str(invalid_credentials, CredentialKey.PASSWORD.value, "BANK_INVALID_PASSWORD")

    accounts = data["accounts"]
    checking = accounts[0]
    savings = accounts[1]

    _override_str(checking, "name", "CHECKING_ACCOUNT_NAME")
    _override_str(checking, "type", "CHECKING_ACCOUNT_TYPE")
    _override_float(checking, "opening_balance", "CHECKING_OPENING_BALANCE")

    _override_str(savings, "name", "SAVINGS_ACCOUNT_NAME")
    _override_str(savings, "type", "SAVINGS_ACCOUNT_TYPE")
    _override_float(savings, "opening_balance", "SAVINGS_OPENING_BALANCE")

    transfer = data["transfer"]
    _override_str(transfer, "from_account", "TRANSFER_FROM")
    _override_str(transfer, "to_account", "TRANSFER_TO")
    _override_float(transfer, "amount", "TRANSFER_AMOUNT")
    _override_str(transfer, "memo", "TRANSFER_MEMO")

    send_money = data["send_money"]
    _override_str(send_money, "from_account", "SEND_FROM")
    _override_float(send_money, "amount", "SEND_AMOUNT")
    _override_str(send_money, "note", "SEND_NOTE")
    _override_str(send_money, "payee_name", "PAYEE_NAME")
    _override_str(send_money, "payee_bank", "PAYEE_BANK")
    _override_str(send_money, "payee_routing", "PAYEE_ROUTING")
    _override_str(send_money, "payee_account", "PAYEE_ACCOUNT")

    bill_pay = data["bill_pay"]
    _override_str(bill_pay, "from_account", "BILL_FROM")
    _override_float(bill_pay, "amount", "BILL_AMOUNT")
    _override_str(bill_pay, "memo", "BILL_MEMO")
    _override_str(bill_pay, "biller_name", "BILLER_NAME")
    _override_str(bill_pay, "biller_reference", "BILLER_REFERENCE")


def _override_str(section: dict[str, Any], key: str, env_name: str) -> None:
    if os.getenv(env_name) is not None:
        section[key] = os.environ[env_name]


def _override_float(section: dict[str, Any], key: str, env_name: str) -> None:
    if os.getenv(env_name) is not None:
        section[key] = float(os.environ[env_name])
