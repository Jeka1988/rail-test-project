"""Internal transfer page object."""

from __future__ import annotations

import re
from typing import Any

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class TransferPage(BasePage):
    path = "/bank/transfer"

    @allure.step("Transfer money between own accounts")
    def transfer_between_accounts(self, transfer_data: dict[str, Any]) -> None:
        self.open()
        self.expect_heading("Transfer Money")

        self.select_option_like_user("From Account", transfer_data["from_account"])
        self.select_option_like_user("To Account", transfer_data["to_account"])
        self.by_test_id_or_label("amount", "Amount").fill(str(transfer_data["amount"]))

        memo = transfer_data.get("memo")
        if memo:
            self._fill_memo(memo)

        self.click_button("Review Transfer")
        self._confirm_review(["Confirm Transfer", "Submit Transfer", "Transfer"])
        self.wait_for_operation_feedback()

    def _confirm_review(self, button_names: list[str]) -> None:
        for name in button_names:
            button = self.page.get_by_role("button", name=name)
            if button.count() > 0:
                expect(button.first).to_be_enabled()
                button.first.click()
                return
        raise AssertionError(f"Could not find transfer confirmation button: {button_names}")

    def _fill_memo(self, memo: str) -> None:
        memo_field = self.page.get_by_test_id("memo")
        if memo_field.count() == 0:
            memo_field = self.page.get_by_placeholder(re.compile("Rent|vacation|memo", re.I))
        if memo_field.count() == 0:
            memo_field = self.page.locator("textarea").first
        expect(memo_field).to_be_visible()
        memo_field.fill(memo)
