"""External send money page object."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Locator, Page, expect

from enums.account import AccountName
from pages.base_page import BasePage


class SendMoneyPage(BasePage):
    path = "/bank/send-money"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Send Money")
        self.from_account_select = page.get_by_label("From Account")
        self.payee_select = page.get_by_test_id("payee-select")
        self.add_payee_button = page.get_by_role("button", name="Add")
        self.add_payee_dialog = page.get_by_test_id("add-payee-dialog")
        self.payee_name_input = page.get_by_test_id("add-payee-name-input")
        self.payee_bank_input = page.get_by_test_id("add-payee-bank-input")
        self.payee_routing_input = page.get_by_test_id("add-payee-routing-input")
        self.payee_account_input = page.get_by_test_id("add-payee-account-input")
        self.save_payee_button = page.get_by_test_id("save-add-payee-btn")
        self.amount_input = page.get_by_label("Amount")
        self.note_input = page.get_by_label("Note (optional)")
        self.review_button = page.get_by_role("button", name="Review & Send")
        self.confirm_button = page.get_by_role("button", name="Confirm Send").or_(
            page.get_by_role("button", name="Send Money")
        ).or_(
            page.get_by_role("button", name="Send")
        )

    def payee_text(self, payee_name: str) -> Locator:
        return self.page.get_by_text(payee_name, exact=True)

    @allure.step("Send money to external payee")
    def send_money(self, send_data: dict[str, Any]) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()

        from_account = AccountName(send_data["from_account"])
        self.select_from_dropdown(self.from_account_select, from_account.value)
        self._ensure_payee(send_data)
        self.amount_input.fill(str(send_data["amount"]))

        note = send_data.get("note")
        if note:
            self.note_input.fill(note)

        self.review_button.click()
        self.confirm_button.first.click()
        self.wait_for_operation_feedback()

    def _ensure_payee(self, send_data: dict[str, Any]) -> None:
        payee_name = send_data["payee_name"]

        if self.payee_text(payee_name).count() > 0:
            self._select_payee(payee_name)
            return

        self.add_payee_button.click()
        expect(self.add_payee_dialog).to_be_visible()
        self.payee_name_input.fill(payee_name)
        self.payee_bank_input.fill(send_data["payee_bank"])
        self.payee_routing_input.fill(send_data["payee_routing"])
        self.payee_account_input.fill(send_data["payee_account"])
        self.save_payee_button.click()
        expect(self.add_payee_dialog).to_be_hidden()
        self._select_payee(payee_name)

    def _select_payee(self, payee_name: str) -> None:
        self.payee_select.click()
        self.visible_option(payee_name).first.click()
