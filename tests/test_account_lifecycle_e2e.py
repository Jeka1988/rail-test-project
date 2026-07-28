from __future__ import annotations

from typing import Any

import pytest
from playwright.sync_api import expect

from enums.account import ScenarioName
from pages.bank_app import BankApp
from utils.money import expected_lifecycle_balances, format_currency


@pytest.mark.e2e
class TestAccountLifecycle:
    """Happy-path coverage for login through financial operations and verification."""

    @pytest.mark.parametrize("scenario_name", [ScenarioName.DEFAULT_ACCOUNT_LIFECYCLE])
    def test_full_account_lifecycle(
        self,
        scenario_name: ScenarioName,
        bank_app: BankApp,
        test_data: dict[str, Any],
    ) -> None:
        """Login, create accounts, transfer/send/bill pay, then assert balances and history."""
        bank_app.start_clean_session()
        bank_app.login(test_data["credentials"])
        expect(bank_app.dashboard_page.welcome_heading).to_be_visible()
        expect(bank_app.dashboard_page.total_net_worth_label).to_be_visible()

        bank_app.create_required_accounts(test_data["accounts"])
        for account in test_data["accounts"]:
            bank_app.accounts_page.open_accounts()
            expect(bank_app.accounts_page.account_text(account["name"])).to_be_visible()

        baseline_net_worth = bank_app.capture_baseline_net_worth()
        bank_app.perform_financial_lifecycle(test_data)

        expected_balances = expected_lifecycle_balances(test_data)
        for account in test_data["accounts"]:
            account_name = account["name"]
            bank_app.accounts_page.open_accounts()
            actual_balance = bank_app.accounts_page.get_account_balance(account_name)
            assert actual_balance == expected_balances[account_name], (
                f"Expected {account_name} balance to be "
                f"{format_currency(expected_balances[account_name])}, "
                f"but got {format_currency(actual_balance)}"
            )

        bank_app.dashboard_page.open()
        actual_net_worth = bank_app.dashboard_page.get_total_net_worth()
        expected_net_worth = (
            baseline_net_worth
            - float(test_data["send_money"]["amount"])
            - float(test_data["bill_pay"]["amount"])
        )
        assert actual_net_worth == expected_net_worth, (
            f"Expected net worth to be {format_currency(expected_net_worth)}, "
            f"but got {format_currency(actual_net_worth)}"
        )

        bank_app.transactions_page.open_transactions()
        expected_entries = [
            (test_data["transfer"]["memo"], test_data["transfer"]["amount"]),
            (test_data["send_money"]["note"], test_data["send_money"]["amount"]),
            (test_data["bill_pay"]["memo"], test_data["bill_pay"]["amount"]),
        ]
        for description, amount in expected_entries:
            expect(
                bank_app.transactions_page.transaction_row(description)
            ).to_be_visible()
            expect(
                bank_app.transactions_page.transaction_amount(
                    description, format_currency(float(amount))
                )
            ).to_be_visible()
