"""Negative login coverage for the Bank Demo app."""

from __future__ import annotations

from typing import Any

import pytest
from playwright.sync_api import expect

from enums.account import LoginErrorMessage
from pages.bank_app import BankApp


@pytest.mark.e2e
class TestLoginNegative:
    """Independent negative login scenarios."""

    def test_login_with_wrong_password(
        self,
        bank_app: BankApp,
        test_data: dict[str, Any],
    ) -> None:
        """Reject login when the password is incorrect and stay on the login page."""
        bank_app.start_clean_session()
        bank_app.attempt_login(test_data["invalid_credentials"])

        expect(bank_app.login_page.login_error_message).to_be_visible()
        expect(bank_app.login_page.login_error_message).to_contain_text(
            LoginErrorMessage.INVALID_CREDENTIALS
        )
        expect(bank_app.login_page.welcome_heading).not_to_be_visible()
