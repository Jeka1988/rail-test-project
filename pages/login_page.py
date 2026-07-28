"""Login page object."""

from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/bank/login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.username_input = page.get_by_test_id("login-username-input")
        self.password_input = page.get_by_test_id("login-password-input")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.welcome_heading = page.get_by_test_id("dashboard-welcome-message")

    @allure.step("Login to Bank Demo")
    def login(self, username: str, password: str) -> None:
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()
        expect(self.welcome_heading).to_be_visible(timeout=15_000)
