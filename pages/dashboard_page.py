"""Dashboard page object."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from utils.money import parse_currency


class DashboardPage(BasePage):
    path = "/bank/dashboard"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.welcome_heading = page.get_by_role("heading", name=re.compile("Welcome", re.I))
        self.total_net_worth_label = page.get_by_text("Total Net Worth")
        self.main_currency_amount = page.locator("main").get_by_text(
            re.compile(r"^\$[\d,]+\.\d{2}$")
        ).first

    def quick_action(self, action_name: str) -> Locator:
        return self.page.get_by_text(action_name, exact=False).first

    def recent_transaction(self, description: str) -> Locator:
        return self.page.get_by_text(description, exact=False).first

    @allure.step("Read total net worth")
    def get_total_net_worth(self) -> float:
        return parse_currency(self.main_currency_amount.inner_text())

    @allure.step("Open quick action")
    def open_quick_action(self, action_name: str) -> None:
        self.quick_action(action_name).click()
