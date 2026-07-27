"""Transactions page object."""

from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class TransactionsPage(BasePage):
    path = "/bank/transactions"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Transactions")

    def transaction_row(self, description: str) -> Locator:
        return self.page.get_by_text(description, exact=False).first.locator("..")

    @allure.step("Open transactions page")
    def open_transactions(self) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()
