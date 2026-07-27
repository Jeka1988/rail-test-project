"""Login page object."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/bank/login"

    @allure.step("Login to Bank Demo")
    def login(self, username: str, password: str) -> None:
        self.open()
        expect(self.page.get_by_role("heading", name="SecureBank")).to_be_visible()

        self.page.get_by_test_id("login-username-input").fill(username)
        self.page.get_by_test_id("login-password-input").fill(password)
        self.click_button("Sign In")

        expect(
            self.page.get_by_role("heading", name=re.compile("Welcome", re.I))
        ).to_be_visible(timeout=15_000)
