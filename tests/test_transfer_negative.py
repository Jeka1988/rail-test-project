"""Negative transfer coverage for the Bank Demo app."""

from __future__ import annotations

from typing import Any

import pytest
from playwright.sync_api import expect

from enums.account import ScenarioName
from pages.bank_app import BankApp
from utils.money import format_currency


@pytest.mark.e2e
class TestTransferNegative:
    """Insufficient-funds transfer scenarios with expected failures."""

    @pytest.mark.parametrize("scenario_name", [ScenarioName.INSUFFICIENT_FUNDS_TRANSFER])
    def test_transfer_with_insufficient_funds(
        self,
        scenario_name: ScenarioName,
        bank_app: BankApp,
        test_data: dict[str, Any],
    ) -> None:
        """Reject an overdraft transfer and leave balances unchanged."""
        scenario = test_data["insufficient_funds"]

        bank_app.start_clean_session()
        bank_app.login(test_data["credentials"])
        expect(bank_app.dashboard_page.welcome_heading).to_be_visible()

        bank_app.create_required_accounts(scenario["accounts"])
        for account in scenario["accounts"]:
            account_name = account["name"]
            bank_app.accounts_page.open_accounts()
            expect(bank_app.accounts_page.account_text(account_name)).to_be_visible()

        baseline_net_worth = bank_app.capture_baseline_net_worth()
        bank_app.attempt_transfer(scenario["transfer"])

        expect(bank_app.transfer_page.transfer_error_message).to_be_visible()
        expect(bank_app.transfer_page.transfer_error_message).to_contain_text(
            "Insufficient funds"
        )

        for account in scenario["accounts"]:
            account_name = account["name"]
            expected_balance = float(account["opening_balance"])
            bank_app.accounts_page.open_accounts()
            actual_balance = bank_app.accounts_page.get_account_balance(account_name)
            assert actual_balance == expected_balance, (
                f"Expected {account_name} balance to remain "
                f"{format_currency(expected_balance)}, "
                f"but got {format_currency(actual_balance)}"
            )

        bank_app.dashboard_page.open()
        actual_net_worth = bank_app.dashboard_page.get_total_net_worth()
        assert actual_net_worth == baseline_net_worth, (
            f"Expected net worth to remain {format_currency(baseline_net_worth)}, "
            f"but got {format_currency(actual_net_worth)}"
        )

        bank_app.transactions_page.open_transactions()
        expect(
            bank_app.transactions_page.transaction_row(scenario["transfer"]["memo"])
        ).not_to_be_visible()
