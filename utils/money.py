from __future__ import annotations

import re
from typing import Any


def parse_currency(value: str | float | int) -> float:
    """Convert UI currency text such as '$1,234.56' into a float."""
    if isinstance(value, (int, float)):
        return float(value)

    cleaned = re.sub(r"[^\d.\-]", "", value)
    if cleaned in {"", "-", "."}:
        raise ValueError(f"Unable to parse currency value: {value!r}")
    return float(cleaned)


def format_currency(amount: float) -> str:
    """Format a numeric amount as USD currency text."""
    return f"${amount:,.2f}"


def expected_lifecycle_balances(test_data: dict[str, Any]) -> dict[str, float]:
    """Compute expected account balances after transfer, send money, and bill pay."""
    balances = {
        account["name"]: float(account["opening_balance"])
        for account in test_data["accounts"]
    }

    transfer = test_data["transfer"]
    balances[transfer["from_account"]] -= float(transfer["amount"])
    balances[transfer["to_account"]] += float(transfer["amount"])

    send_money = test_data["send_money"]
    balances[send_money["from_account"]] -= float(send_money["amount"])

    bill_pay = test_data["bill_pay"]
    balances[bill_pay["from_account"]] -= float(bill_pay["amount"])

    balances["net_worth"] = sum(balances.values())
    return balances
