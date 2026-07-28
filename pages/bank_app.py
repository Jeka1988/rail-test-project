"""High-level Bank Demo facade used by tests."""

from __future__ import annotations

from typing import Any

import allure

from enums.account import CredentialKey, PageName
from pages.accounts_page import AccountsPage
from pages.bill_pay_page import BillPayPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.send_money_page import SendMoneyPage
from pages.transactions_page import TransactionsPage
from pages.transfer_page import TransferPage


class BankApp:
    """
    Composes page objects into business-level lifecycle actions.

    Tests call this facade for actions and perform business assertions themselves.
    """

    def __init__(self, pages: dict[str, object]) -> None:
        self.login_page: LoginPage = pages[PageName.LOGIN.value]  # type: ignore[assignment]
        self.dashboard_page: DashboardPage = pages[PageName.DASHBOARD.value]  # type: ignore[assignment]
        self.accounts_page: AccountsPage = pages[PageName.ACCOUNTS.value]  # type: ignore[assignment]
        self.transfer_page: TransferPage = pages[PageName.TRANSFER.value]  # type: ignore[assignment]
        self.send_money_page: SendMoneyPage = pages[PageName.SEND_MONEY.value]  # type: ignore[assignment]
        self.bill_pay_page: BillPayPage = pages[PageName.BILL_PAY.value]  # type: ignore[assignment]
        self.transactions_page: TransactionsPage = pages[PageName.TRANSACTIONS.value]  # type: ignore[assignment]

    @allure.step("Start from clean Bank Demo session")
    def start_clean_session(self) -> None:
        self.login_page.reset_browser_storage()

    @allure.step("Login as configured user")
    def login(self, credentials: dict[str, str]) -> None:
        self.login_page.login(
            credentials[CredentialKey.USERNAME.value],
            credentials[CredentialKey.PASSWORD.value],
        )

    @allure.step("Attempt login with provided credentials")
    def attempt_login(self, credentials: dict[str, str]) -> None:
        self.login_page.submit_login(
            credentials[CredentialKey.USERNAME.value],
            credentials[CredentialKey.PASSWORD.value],
        )

    @allure.step("Create required lifecycle accounts")
    def create_required_accounts(self, accounts: list[dict[str, Any]]) -> None:
        for account in accounts:
            self.accounts_page.create_account(account)

    @allure.step("Capture baseline net worth")
    def capture_baseline_net_worth(self) -> float:
        self.dashboard_page.open()
        return self.dashboard_page.get_total_net_worth()

    @allure.step("Attempt transfer with provided data")
    def attempt_transfer(self, transfer_data: dict[str, Any]) -> None:
        self.transfer_page.submit_transfer(transfer_data)

    @allure.step("Perform account lifecycle financial operations")
    def perform_financial_lifecycle(self, test_data: dict[str, Any]) -> None:
        self.transfer_page.transfer_between_accounts(test_data["transfer"])
        self.send_money_page.send_money(test_data["send_money"])
        self.bill_pay_page.pay_bill(test_data["bill_pay"])
