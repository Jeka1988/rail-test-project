from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class TransactionsPage(BasePage):
    path = "/bank/transactions"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Transactions")
        self.transaction_entries = page.get_by_test_id("all-txn-row")
        self.transaction_amounts = page.get_by_test_id("all-txn-amount")

    def transaction_row(self, description: str) -> Locator:
        return self.transaction_entries.filter(has_text=description).first

    def transaction_amount(self, description: str, amount: str) -> Locator:
        return self.transaction_row(description).locator(self.transaction_amounts).filter(
            has_text=amount
        )

    @allure.step("Open transactions page")
    def open_transactions(self) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()
