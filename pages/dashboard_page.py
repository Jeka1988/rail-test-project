from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.money import parse_currency


class DashboardPage(BasePage):
    path = "/bank/dashboard"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.welcome_heading = page.get_by_test_id("dashboard-welcome-message")
        self.total_net_worth_label = page.get_by_test_id("stat-card-net-worth-label")
        self.main_currency_amount = page.get_by_test_id("stat-card-net-worth-value")

    @allure.step("Read total net worth")
    def get_total_net_worth(self) -> float:
        """Return the dashboard total net worth as a float."""
        return parse_currency(self.main_currency_amount.inner_text())
