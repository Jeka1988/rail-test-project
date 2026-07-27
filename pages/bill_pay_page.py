"""Bill pay page object."""

from __future__ import annotations

from typing import Any

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class BillPayPage(BasePage):
    path = "/bank/bill-pay"

    @allure.step("Pay a bill")
    def pay_bill(self, bill_data: dict[str, Any]) -> None:
        self.open()
        self.expect_heading("Pay a Bill")

        self.select_option_like_user("From Account", bill_data["from_account"])
        self._ensure_biller(bill_data)
        self.page.get_by_test_id("bill-amount-input").fill(str(bill_data["amount"]))

        memo = bill_data.get("memo")
        if memo:
            self.page.get_by_test_id("bill-memo-input").fill(memo)

        self.page.get_by_test_id("review-bill-btn").click()
        self._click_first_available_button(["Confirm Payment", "Submit Payment", "Pay Bill", "Pay"])
        self.wait_for_operation_feedback()

    def _ensure_biller(self, bill_data: dict[str, Any]) -> None:
        biller_name = bill_data["biller_name"]
        self.page.get_by_test_id("add-biller-btn").click()
        expect(self.page.get_by_test_id("add-biller-dialog")).to_be_visible()
        self.page.get_by_test_id("add-biller-name-input").fill(biller_name)
        self.page.locator("input[name='biller_ref_field']").fill(
            bill_data["biller_reference"]
        )
        self.page.get_by_test_id("save-add-biller-btn").click()
        expect(self.page.get_by_test_id("add-biller-dialog")).to_be_hidden()

        search = self.page.get_by_test_id("biller-search-input")
        search.fill(biller_name)
        result = self.page.locator("[role='option']:visible").filter(has_text=biller_name)
        if result.count() == 0:
            result = self.page.get_by_text(biller_name, exact=False)
        expect(result.first).to_be_visible()
        result.first.click()

    def _click_first_available_button(self, names: list[str]) -> None:
        for name in names:
            button = self.page.get_by_role("button", name=name)
            if button.count() > 0:
                expect(button.first).to_be_enabled()
                button.first.click()
                return
        raise AssertionError(f"Could not find any button named: {names}")
