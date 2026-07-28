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
    def __init__(self, pages: dict[str, Any]) -> None:
        self.login_page: LoginPage = pages[PageName.LOGIN.value]
        self.dashboard_page: DashboardPage = pages[PageName.DASHBOARD.value]
        self.accounts_page: AccountsPage = pages[PageName.ACCOUNTS.value]
        self.transfer_page: TransferPage = pages[PageName.TRANSFER.value]
        self.send_money_page: SendMoneyPage = pages[PageName.SEND_MONEY.value]
        self.bill_pay_page: BillPayPage = pages[PageName.BILL_PAY.value]
        self.transactions_page: TransactionsPage = pages[PageName.TRANSACTIONS.value]

    @allure.step("Start from clean Bank Demo session")
    def start_clean_session(self) -> None:
        """Reset browser storage so the run does not depend on prior state."""
        self.login_page.reset_browser_storage()

    @allure.step("Login as configured user")
    def login(self, credentials: dict[str, str]) -> None:
        """Log in with valid credentials and reach the dashboard."""
        self.login_page.login(
            credentials[CredentialKey.USERNAME.value],
            credentials[CredentialKey.PASSWORD.value],
        )

    @allure.step("Attempt login with provided credentials")
    def attempt_login(self, credentials: dict[str, str]) -> None:
        """Submit login without asserting success (for negative cases)."""
        self.login_page.submit_login(
            credentials[CredentialKey.USERNAME.value],
            credentials[CredentialKey.PASSWORD.value],
        )

    @allure.step("Create required lifecycle accounts")
    def create_required_accounts(self, accounts: list[dict[str, Any]]) -> None:
        """Create each account described in the scenario data."""
        for account in accounts:
            self.accounts_page.create_account(account)

    @allure.step("Capture baseline net worth")
    def capture_baseline_net_worth(self) -> float:
        """Open the dashboard and return the current total net worth."""
        self.dashboard_page.open()
        return self.dashboard_page.get_total_net_worth()

    @allure.step("Attempt transfer with provided data")
    def attempt_transfer(self, transfer_data: dict[str, Any]) -> None:
        """Submit a transfer without waiting for success (for negative cases)."""
        self.transfer_page.submit_transfer(transfer_data)

    @allure.step("Perform account lifecycle financial operations")
    def perform_financial_lifecycle(self, test_data: dict[str, Any]) -> None:
        """Run transfer, send money, and bill pay from the scenario data."""
        self.transfer_page.transfer_between_accounts(test_data["transfer"])
        self.send_money_page.send_money(test_data["send_money"])
        self.bill_pay_page.pay_bill(test_data["bill_pay"])
