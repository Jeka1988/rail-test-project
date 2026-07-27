"""Shared page-object functionality."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Base class with navigation and stable waiting helpers."""

    path = "/bank"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    @property
    def app_origin(self) -> str:
        return self.base_url.rsplit("/bank", maxsplit=1)[0]

    @property
    def url(self) -> str:
        return f"{self.app_origin}{self.path}"

    @allure.step("Open page")
    def open(self) -> None:
        self.page.goto(self.url, wait_until="domcontentloaded")

    @allure.step("Reset browser storage for clean test state")
    def reset_browser_storage(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        self.page.reload(wait_until="domcontentloaded")

    def by_test_id_or_label(self, test_id: str, label: str) -> Locator:
        """Prefer data-testid, then fall back to accessible label."""
        by_test_id = self.page.get_by_test_id(test_id)
        if by_test_id.count() > 0:
            return by_test_id
        return self.page.get_by_label(label)

    def click_button(self, name: str) -> None:
        button = self.page.get_by_role("button", name=name)
        expect(button).to_be_enabled()
        button.click()

    def navigate_to(self, name: str) -> None:
        link = self.page.get_by_role("link", name=name)
        expect(link).to_be_visible()
        link.click()

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()

    def expect_text(self, text: str | Locator) -> None:
        if isinstance(text, str):
            expect(self.page.get_by_text(text, exact=False).first).to_be_visible()
        else:
            expect(text).to_be_visible()

    def select_option_like_user(self, label: str, value: str) -> None:
        """
        Select an option from a native select or custom dropdown.

        The Bank Demo app has changed over time, so this handles both common UI
        patterns without leaking selector logic into tests.
        """
        field = self.page.get_by_label(label)
        expect(field).to_be_visible()

        tag_name = field.evaluate("element => element.tagName.toLowerCase()")
        if tag_name == "select":
            field.select_option(label=value)
            return

        field.click()
        option = self.page.locator("[role='option']:visible").filter(has_text=value)
        if option.count() == 0:
            option = self.page.locator("[role='listbox']:visible").get_by_text(value, exact=False)
        expect(option.first).to_be_visible()
        option.first.click()

    def wait_for_operation_feedback(self) -> None:
        """Wait for a toast/alert/dialog feedback after a submitted action."""
        feedback = self.page.get_by_role("alert").or_(
            self.page.locator("[data-testid*='success']")
        ).or_(
            self.page.get_by_text(re.compile(r"success|completed|transferred|sent|paid", re.I))
        )
        expect(feedback.first).to_be_visible(timeout=10_000)
