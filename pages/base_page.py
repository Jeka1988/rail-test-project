"""Shared page-object functionality."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Base class with navigation and shared action helpers."""

    path = "/bank"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.success_feedback = page.get_by_role("alert").or_(
            page.get_by_test_id(re.compile(r".*success.*"))
        ).or_(
            page.get_by_text(re.compile(r"success|completed|transferred|sent|paid", re.I))
        )
        self.options = page.get_by_role("option")

    @property
    def app_origin(self) -> str:
        return self.base_url.rsplit("/bank", maxsplit=1)[0]

    @property
    def url(self) -> str:
        return f"{self.app_origin}{self.path}"

    @allure.step("Open page")
    def open(self) -> None:
        self.page.goto(self.url)

    @allure.step("Reset browser storage for clean test state")
    def reset_browser_storage(self) -> None:
        self.page.goto(self.base_url)
        self.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        self.page.reload()

    def option_by_name(self, text: str) -> Locator:
        """Return a dropdown option by accessible name / visible text."""
        return self.options.filter(has_text=text)

    def select_from_dropdown(self, dropdown: Locator, value: str) -> None:
        """Select a value from a page-owned dropdown locator."""
        dropdown.click()
        self.option_by_name(value).first.click()

    def wait_for_operation_feedback(self) -> None:
        """Wait until the UI confirms the submitted action finished."""
        expect(self.success_feedback.first).to_be_visible(timeout=10_000)
