"""High-level Bank Demo facade used by tests."""

from __future__ import annotations

from typing import Any

import allure

from pages.accounts_page import AccountsPage
from pages.bill_pay_page import BillPayPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.send_money_page import SendMoneyPage
from pages.transactions_page import TransactionsPage
from pages.transfer_page import TransferPage
from utils.money import expected_lifecycle_balances, format_currency


class BankApp:
    """
    Composes page objects into business-level lifecycle actions.

    Tests call this facade to avoid raw UI interactions in test files while all
    selectors and waits remain inside the page-object layer.
    """

    def __init__(self, pages: dict[str, object]) -> None:
        self.login_page: LoginPage = pages["login"]  # type: ignore[assignment]
        self.dashboard_page: DashboardPage = pages["dashboard"]  # type: ignore[assignment]
        self.accounts_page: AccountsPage = pages["accounts"]  # type: ignore[assignment]
        self.transfer_page: TransferPage = pages["transfer"]  # type: ignore[assignment]
        self.send_money_page: SendMoneyPage = pages["send_money"]  # type: ignore[assignment]
        self.bill_pay_page: BillPayPage = pages["bill_pay"]  # type: ignore[assignment]
        self.transactions_page: TransactionsPage = pages["transactions"]  # type: ignore[assignment]
        self.baseline_net_worth: float | None = None

    @allure.step("Start from clean Bank Demo session")
    def start_clean_session(self) -> None:
        self.login_page.reset_browser_storage()

    @allure.step("Login as configured user")
    def login(self, credentials: dict[str, str]) -> None:
        self.login_page.login(credentials["username"], credentials["password"])
        self.dashboard_page.assert_loaded()

    @allure.step("Create required lifecycle accounts")
    def create_required_accounts(self, accounts: list[dict[str, Any]]) -> None:
        for account in accounts:
            self.accounts_page.create_account(account)

    @allure.step("Perform account lifecycle financial operations")
    def perform_financial_lifecycle(self, test_data: dict[str, Any]) -> None:
        self.dashboard_page.open()
        self.dashboard_page.assert_loaded()
        self.baseline_net_worth = self.dashboard_page.get_total_net_worth()
        self.transfer_page.transfer_between_accounts(test_data["transfer"])
        self.send_money_page.send_money(test_data["send_money"])
        self.bill_pay_page.pay_bill(test_data["bill_pay"])

    @allure.step("Verify final lifecycle results")
    def assert_lifecycle_results(self, test_data: dict[str, Any]) -> None:
        expected_balances = expected_lifecycle_balances(test_data)

        for account in test_data["accounts"]:
            account_name = account["name"]
            self.accounts_page.assert_account_balance(account_name, expected_balances[account_name])

        self.dashboard_page.open()
        self.dashboard_page.assert_loaded()
        actual_net_worth = self.dashboard_page.get_total_net_worth()
        assert self.baseline_net_worth is not None, "Baseline net worth was not captured"
        expected_net_worth = (
            self.baseline_net_worth
            - float(test_data["send_money"]["amount"])
            - float(test_data["bill_pay"]["amount"])
        )
        assert actual_net_worth == expected_net_worth, (
            f"Expected net worth to be {format_currency(expected_net_worth)}, "
            f"but got {format_currency(actual_net_worth)}"
        )

        self.transactions_page.assert_lifecycle_transactions(test_data)
