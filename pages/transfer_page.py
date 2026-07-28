"""Internal transfer page object."""

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
        self.confirm_button = page.get_by_role("button", name="Confirm Transfer").or_(
            page.get_by_role("button", name="Submit Transfer")
        ).or_(
            page.get_by_role("button", name="Transfer")
        )

    @allure.step("Transfer money between own accounts")
    def transfer_between_accounts(self, transfer_data: dict[str, Any]) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()

        self.select_from_dropdown(self.from_account_select, transfer_data["from_account"])
        self.select_from_dropdown(self.to_account_select, transfer_data["to_account"])
        self.amount_input.fill(str(transfer_data["amount"]))

        memo = transfer_data.get("memo")
        if memo:
            self.memo_input.fill(memo)

        self.review_button.click()
        self.confirm_button.first.click()
        self.wait_for_operation_feedback()
