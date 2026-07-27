"""External send money page object."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class SendMoneyPage(BasePage):
    path = "/bank/send-money"

    @allure.step("Send money to external payee")
    def send_money(self, send_data: dict[str, Any]) -> None:
        self.open()
        self.expect_heading("Send Money")

        self.select_option_like_user("From Account", send_data["from_account"])
        self._ensure_payee(send_data)
        self.by_test_id_or_label("amount", "Amount").fill(str(send_data["amount"]))

        note = send_data.get("note")
        if note:
            self.by_test_id_or_label("note", "Note (optional)").fill(note)

        self.click_button("Review & Send")
        self._confirm_review(["Confirm Send", "Send Money", "Send"])
        self.wait_for_operation_feedback()

    def _ensure_payee(self, send_data: dict[str, Any]) -> None:
        payee_name = send_data["payee_name"]
        payee_picker = self.page.get_by_test_id("payee-select")
        if payee_picker.count() == 0:
            payee_picker = self.page.get_by_label("Payee")
        expect(payee_picker.first).to_be_visible()

        if self.page.get_by_text(payee_name, exact=True).count() > 0:
            self._select_payee(payee_name)
            return

        self.click_button("Add")
        expect(self.page.get_by_test_id("add-payee-dialog")).to_be_visible()
        self.page.get_by_test_id("add-payee-name-input").fill(payee_name)
        self.page.get_by_test_id("add-payee-bank-input").fill(send_data["payee_bank"])
        self.page.get_by_test_id("add-payee-routing-input").fill(send_data["payee_routing"])
        self.page.get_by_test_id("add-payee-account-input").fill(send_data["payee_account"])
        self.page.get_by_test_id("save-add-payee-btn").click()
        expect(self.page.get_by_test_id("add-payee-dialog")).to_be_hidden()
        self._select_payee(payee_name)

    def _select_payee(self, payee_name: str) -> None:
        picker = self.page.get_by_test_id("payee-select")
        if picker.count() == 0:
            picker = self.page.get_by_label("Payee")
        expect(picker.first).to_be_visible()
        picker.first.click()
        option = self.page.locator("[role='option']:visible").filter(has_text=payee_name)
        expect(option.first).to_be_visible()
        option.first.click()

    def _fill_optional_field(self, test_ids: list[str], labels: list[str], value: str) -> None:
        for test_id in test_ids:
            locator = self.page.get_by_test_id(test_id)
            if locator.count() > 0:
                locator.first.fill(value)
                return
        for label in labels:
            locator = self.page.get_by_label(label)
            if locator.count() > 0:
                locator.first.fill(value)
                return

    def _click_first_available_button(self, names: list[str]) -> None:
        for name in names:
            button = self.page.get_by_role("button", name=name)
            if button.count() > 0:
                expect(button.first).to_be_enabled()
                button.first.click()
                return
        raise AssertionError(f"Could not find any button named: {names}")

    def _confirm_review(self, button_names: list[str]) -> None:
        self._click_first_available_button(button_names)
