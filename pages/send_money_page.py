"""External send money page object."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class SendMoneyPage(BasePage):
    path = "/bank/send-money"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Send Money")
        self.from_account_select = page.get_by_test_id("send-from-account-select")
        self.payee_select = page.get_by_test_id("payee-select")
        self.add_payee_button = page.get_by_test_id("add-payee-btn")
        self.add_payee_dialog = page.get_by_test_id("add-payee-dialog")
        self.payee_name_input = page.get_by_test_id("add-payee-name-input")
        self.payee_bank_input = page.get_by_test_id("add-payee-bank-input")
        self.payee_routing_input = page.get_by_test_id("add-payee-routing-input")
        self.payee_account_input = page.get_by_test_id("add-payee-account-input")
        self.save_payee_button = page.get_by_test_id("save-add-payee-btn")
        self.amount_input = page.get_by_test_id("send-amount-input")
        self.note_input = page.get_by_test_id("send-note-input")
        self.review_button = page.get_by_test_id("review-send-btn")
        self.confirm_button = page.get_by_role("button", name="Confirm Send").or_(
            page.get_by_role("button", name="Send Money")
        ).or_(
            page.get_by_role("button", name="Send")
        )

    @allure.step("Send money to external payee")
    def send_money(self, send_data: dict[str, Any]) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()

        self.select_from_dropdown(self.from_account_select, send_data["from_account"])
        self._ensure_payee(send_data)
        self.amount_input.fill(str(send_data["amount"]))

        note = send_data.get("note")
        if note:
            self.note_input.fill(note)

        self.review_button.click()
        self.confirm_button.first.click()
        self.wait_for_operation_feedback()

    def _ensure_payee(self, send_data: dict[str, Any]) -> None:
        """Create the payee when missing, then select it.

        Avoid opening the payee combobox before Add — Base UI leaves a portal
        backdrop that intercepts the Add button click.
        """
        payee_name = send_data["payee_name"]
        self.add_payee_button.click()
        expect(self.add_payee_dialog).to_be_visible()
        self.payee_name_input.fill(payee_name)
        self.payee_bank_input.fill(send_data["payee_bank"])
        self.payee_routing_input.fill(send_data["payee_routing"])
        self.payee_account_input.fill(send_data["payee_account"])
        self.save_payee_button.click()
        expect(self.add_payee_dialog).to_be_hidden()
        self.select_from_dropdown(self.payee_select, payee_name)
