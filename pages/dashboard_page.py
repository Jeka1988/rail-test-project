"""Dashboard page object."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.money import parse_currency


class DashboardPage(BasePage):
    path = "/bank/dashboard"

    @allure.step("Verify dashboard is loaded")
    def assert_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name=re.compile("Welcome", re.I))).to_be_visible()
        expect(self.page.get_by_text("Total Net Worth")).to_be_visible()

    @allure.step("Read total net worth")
    def get_total_net_worth(self) -> float:
        amount = self.page.locator("main").get_by_text(
            re.compile(r"^\$[\d,]+\.\d{2}$")
        ).first
        expect(amount).to_be_visible()
        return parse_currency(amount.inner_text())

    @allure.step("Open quick action")
    def open_quick_action(self, action_name: str) -> None:
        quick_action = self.page.get_by_text(action_name, exact=False).first
        expect(quick_action).to_be_visible()
        quick_action.click()

    @allure.step("Verify recent transaction appears")
    def assert_recent_transaction(self, description: str) -> None:
        expect(self.page.get_by_text(description, exact=False).first).to_be_visible()
