"""Accounts page object."""

from __future__ import annotations

import re
from typing import Any

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.money import format_currency, parse_currency


class AccountsPage(BasePage):
    path = "/bank/accounts"

    @allure.step("Open accounts page")
    def open_accounts(self) -> None:
        self.open()
        self.expect_heading("My Accounts")

    @allure.step("Create bank account")
    def create_account(self, account: dict[str, Any]) -> None:
        self.open_accounts()
        self.click_button("Add Account")

        if self.page.get_by_test_id("account-form").count() > 0:
            self._create_account_with_current_modal(account)
            self.assert_account_visible(account["name"])
            return

        self._fill_if_present(["account-name", "name"], ["Account Name", "Name"], account["name"])
        self._select_if_present(
            ["account-type", "type"],
            ["Account Type", "Type"],
            account["type"],
        )
        self._fill_if_present(
            ["opening-balance", "initial-balance", "balance"],
            ["Opening Balance", "Initial Balance", "Balance"],
            str(account["opening_balance"]),
        )

        self._click_first_available_button(["Save Account", "Create Account", "Add Account", "Save"])
        self.assert_account_visible(account["name"])

    def _create_account_with_current_modal(self, account: dict[str, Any]) -> None:
        expect(self.page.get_by_test_id("add-account-dialog")).to_be_visible()
        self.page.get_by_test_id("account-form-name-input").fill(account["name"])
        self.page.get_by_test_id("account-form-type-select").click()
        option = self.page.get_by_role("option", name=account["type"])
        expect(option).to_be_visible()
        option.click()
        self.page.locator("input[name='account_balance_field']").fill(
            str(account["opening_balance"])
        )
        terms = self.page.get_by_test_id("account-form-accept-terms-checkbox")
        if terms.count() > 0:
            terms.click()
        self.page.get_by_test_id("save-account-form-btn").click()

    @allure.step("Verify account is visible")
    def assert_account_visible(self, account_name: str) -> None:
        expect(self.page.get_by_text(account_name, exact=False).first).to_be_visible()

    @allure.step("Read account balance")
    def get_account_balance(self, account_name: str) -> float:
        account_row = self.page.get_by_role(
            "row",
            name=re.compile(re.escape(account_name)),
        )
        amount = account_row.get_by_text(re.compile(r"\$[\d,]+\.\d{2}")).first
        expect(amount).to_be_visible()
        return parse_currency(amount.inner_text())

    @allure.step("Verify account balance")
    def assert_account_balance(self, account_name: str, expected_amount: float) -> None:
        self.open_accounts()
        balance = self.get_account_balance(account_name)
        assert balance == expected_amount, (
            f"Expected {account_name} balance to be {format_currency(expected_amount)}, "
            f"but got {format_currency(balance)}"
        )

    def _fill_if_present(self, test_ids: list[str], labels: list[str], value: str) -> None:
        field = self._first_visible_field(test_ids, labels)
        expect(field).to_be_visible()
        field.fill(value)

    def _select_if_present(self, test_ids: list[str], labels: list[str], value: str) -> None:
        field = self._first_visible_field(test_ids, labels)
        expect(field).to_be_visible()
        tag_name = field.evaluate("element => element.tagName.toLowerCase()")
        if tag_name == "select":
            field.select_option(label=value)
            return
        field.click()
        option = self.page.get_by_role("option", name=value)
        if option.count() == 0:
            option = self.page.locator("[role='listbox']").get_by_text(value, exact=True)
        expect(option.first).to_be_visible()
        option.first.click()

    def _first_visible_field(self, test_ids: list[str], labels: list[str]):
        for test_id in test_ids:
            locator = self.page.get_by_test_id(test_id)
            if locator.count() > 0:
                return locator.first
        for label in labels:
            locator = self.page.get_by_label(label)
            if locator.count() > 0:
                return locator.first
        raise AssertionError(f"Could not find field by test ids {test_ids} or labels {labels}")

    def _click_first_available_button(self, names: list[str]) -> None:
        for name in names:
            button = self.page.get_by_role("button", name=name)
            if button.count() > 0:
                expect(button.first).to_be_enabled()
                button.first.click()
                return
        raise AssertionError(f"Could not find any button named: {names}")
