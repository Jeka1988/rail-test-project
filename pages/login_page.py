from __future__ import annotations

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/bank/login"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.username_input = page.get_by_test_id("login-username-input")
        self.password_input = page.get_by_test_id("login-password-input")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.welcome_heading = page.get_by_test_id("dashboard-welcome-message")
        self.login_error_message = page.get_by_test_id("login-error-message")

    @allure.step("Submit login form")
    def submit_login(self, username: str, password: str) -> None:
        """Fill credentials and click Sign In without asserting success."""
        self.open()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()

    @allure.step("Login to Bank Demo")
    def login(self, username: str, password: str) -> None:
        """Submit valid credentials on the login form."""
        self.submit_login(username, password)
