"""Transactions page object."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.money import format_currency


class TransactionsPage(BasePage):
    path = "/bank/transactions"

    @allure.step("Open transactions page")
    def open_transactions(self) -> None:
        self.open()
        self.expect_heading("Transactions")

    @allure.step("Verify lifecycle transactions are present")
    def assert_lifecycle_transactions(self, test_data: dict[str, Any]) -> None:
        self.open_transactions()
        expected_entries = [
            (test_data["transfer"]["memo"], test_data["transfer"]["amount"]),
            (test_data["send_money"]["note"], test_data["send_money"]["amount"]),
            (test_data["bill_pay"]["memo"], test_data["bill_pay"]["amount"]),
        ]

        for description, amount in expected_entries:
            self.assert_transaction_exists(description, float(amount))

    @allure.step("Verify transaction exists")
    def assert_transaction_exists(self, description: str, amount: float) -> None:
        transaction_row = self.page.get_by_text(description, exact=False).first.locator("..")
        expect(transaction_row).to_be_visible()
        expect(transaction_row.get_by_text(format_currency(amount))).to_be_visible()
