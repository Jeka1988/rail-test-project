from __future__ import annotations

import re
from typing import Any

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class BillPayPage(BasePage):
    path = "/bank/bill-pay"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="Pay a Bill")
        self.from_account_select = page.get_by_test_id("bill-pay-from-select")
        self.add_biller_button = page.get_by_test_id("add-biller-btn")
        self.add_biller_dialog = page.get_by_test_id("add-biller-dialog")
        self.biller_name_input = page.get_by_test_id("add-biller-name-input")
        self.biller_reference_input = self.add_biller_dialog.get_by_placeholder(
            re.compile(r"ACC-", re.I)
        )
        self.save_biller_button = page.get_by_test_id("save-add-biller-btn")
        self.biller_search_input = page.get_by_test_id("biller-search-input")
        self.amount_input = page.get_by_test_id("bill-amount-input")
        self.memo_input = page.get_by_test_id("bill-memo-input")
        self.review_button = page.get_by_test_id("review-bill-btn")
        self.confirm_button = page.get_by_role("button", name="Confirm Payment").or_(
            page.get_by_role("button", name="Submit Payment")
        ).or_(
            page.get_by_role("button", name="Pay Bill")
        ).or_(
            page.get_by_role("button", name="Pay")
        )

    @allure.step("Pay a bill")
    def pay_bill(self, bill_data: dict[str, Any]) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()

        self.select_from_dropdown(self.from_account_select, bill_data["from_account"])
        self._ensure_biller(bill_data)
        self.amount_input.fill(str(bill_data["amount"]))

        memo = bill_data.get("memo")
        if memo:
            self.memo_input.fill(memo)

        self.review_button.click()
        self.confirm_button.first.click()
        self.wait_for_operation_feedback()

    def _ensure_biller(self, bill_data: dict[str, Any]) -> None:
        biller_name = bill_data["biller_name"]
        self.add_biller_button.click()
        expect(self.add_biller_dialog).to_be_visible()
        self.biller_name_input.fill(biller_name)
        self.biller_reference_input.fill(bill_data["biller_reference"])
        self.save_biller_button.click()
        expect(self.add_biller_dialog).to_be_hidden()

        self.biller_search_input.fill(biller_name)
        self.option_by_name(biller_name).first.click()
