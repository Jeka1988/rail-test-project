"""Accounts page object."""

from __future__ import annotations

import re
from typing import Any

import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from utils.money import parse_currency


class AccountsPage(BasePage):
    path = "/bank/accounts"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.page_heading = page.get_by_role("heading", name="My Accounts")
        self.add_account_button = page.get_by_role("button", name="Add Account")
        self.add_account_dialog = page.get_by_test_id("add-account-dialog")
        self.account_form = page.get_by_test_id("account-form")
        self.account_name_input = page.get_by_test_id("account-form-name-input")
        self.account_type_select = page.get_by_test_id("account-form-type-select")
        self.opening_balance_input = page.locator("input[name='account_balance_field']")
        self.accept_terms_checkbox = page.get_by_test_id("account-form-accept-terms-checkbox")
        self.save_account_button = page.get_by_test_id("save-account-form-btn")

    def account_text(self, account_name: str) -> Locator:
        return self.page.get_by_text(account_name, exact=False).first

    def account_row(self, account_name: str) -> Locator:
        return self.page.get_by_role("row", name=re.compile(re.escape(account_name)))

    @allure.step("Open accounts page")
    def open_accounts(self) -> None:
        self.open()
        expect(self.page_heading).to_be_visible()

    @allure.step("Create bank account")
    def create_account(self, account: dict[str, Any]) -> None:
        self.open_accounts()
        self.add_account_button.click()
        expect(self.add_account_dialog).to_be_visible()

        self.account_name_input.fill(account["name"])
        self.select_from_dropdown(self.account_type_select, account["type"])
        self.opening_balance_input.fill(str(account["opening_balance"]))

        if self.accept_terms_checkbox.count() > 0:
            self.accept_terms_checkbox.click()

        self.save_account_button.click()
        expect(self.add_account_dialog).to_be_hidden()

    @allure.step("Read account balance")
    def get_account_balance(self, account_name: str) -> float:
        amount = self.account_row(account_name).get_by_text(re.compile(r"\$[\d,]+\.\d{2}")).first
        return parse_currency(amount.inner_text())
