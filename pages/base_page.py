from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    path = "/bank"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.success_feedback = page.get_by_role("alert")
        self.options = page.get_by_role("option")

    @property
    def app_origin(self) -> str:
        return self.base_url.rsplit("/bank", maxsplit=1)[0]

    @property
    def url(self) -> str:
        return f"{self.app_origin}{self.path}"

    @allure.step("Open page")
    def open(self) -> None:
        """Navigate to this page's URL."""
        self.page.goto(self.url)

    @allure.step("Reset browser storage for clean test state")
    def reset_browser_storage(self) -> None:
        """Clear localStorage/sessionStorage and reload for an independent run."""
        self.page.goto(self.base_url)
        self.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        self.page.reload()

    def _matching_option(self, value: str) -> Locator:
        """Visible option whose accessible name starts with the value."""
        return self.page.get_by_role(
            "option",
            name=re.compile(rf"^{re.escape(value)}(?:\s|$)"),
        ).locator("visible=true")

    def _select_from_dropdown(self, dropdown: Locator, value: str) -> None:
        """Open a dropdown and choose the visible option that matches the value."""
        dropdown.click()
        option = self._matching_option(value)
        expect(option).to_be_visible()
        option.click()

    def _wait_for_operation_feedback(self) -> None:
        """Wait until the success alert confirms the action finished."""
        expect(self.success_feedback).to_be_visible()
