from __future__ import annotations

import re
from typing import Any

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class TransferPage(BasePage):
    path = "/bank/transfer"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Transfer Money")
        self.transfer_form = page.get_by_test_id("transfer-form")
        self.from_account_select = page.get_by_test_id("transfer-from-select")
        self.to_account_select = page.get_by_test_id("transfer-to-select")
        self.amount_input = page.get_by_test_id("transfer-amount-input")
        self.memo_input = self.transfer_form.get_by_placeholder(
            re.compile(r"Rent|vacation", re.I)
        )
        self.review_button = page.get_by_test_id("review-transfer-btn")
        self.confirm_button = page.get_by_test_id("confirm-transfer-btn")
        self.transfer_error_message = page.get_by_test_id("transfer-error-message")

    def _fill_transfer_form(self, transfer_data: dict[str, Any]) -> None:
        """Fill transfer fields through review; does not confirm."""
        self._select_from_dropdown(self.from_account_select, transfer_data["from_account"])
        self._select_from_dropdown(self.to_account_select, transfer_data["to_account"])
        self.amount_input.fill(str(transfer_data["amount"]))

        memo = transfer_data.get("memo")
        if memo:
            self.memo_input.fill(memo)

        self.review_button.click()

    @allure.step("Submit transfer without waiting for success")
    def submit_transfer(self, transfer_data: dict[str, Any]) -> None:
        """Submit a transfer and leave success/error handling to the caller."""
        self.open()
        expect(self.page_heading).to_be_visible()
        self._fill_transfer_form(transfer_data)
        self.confirm_button.click()

    @allure.step("Transfer money between own accounts")
    def transfer_between_accounts(self, transfer_data: dict[str, Any]) -> None:
        """Complete a successful internal transfer and wait for confirmation."""
        self.submit_transfer(transfer_data)
        self._wait_for_operation_feedback()
