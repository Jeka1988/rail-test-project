"""End-to-end account lifecycle coverage for the Bank Demo app."""

from __future__ import annotations

from typing import Any

import pytest

from pages.bank_app import BankApp


@pytest.mark.e2e
class TestAccountLifecycle:
    """pytest equivalent of Playwright Test's test.describe block."""

    @pytest.mark.parametrize("scenario_name", ["default_account_lifecycle"])
    def test_full_account_lifecycle(
        self,
        scenario_name: str,
        bank_app: BankApp,
        test_data: dict[str, Any],
    ) -> None:
        """Cover login, accounts, financial operations, and final verification."""
        assert scenario_name
        bank_app.start_clean_session()
        bank_app.login(test_data["credentials"])
        bank_app.create_required_accounts(test_data["accounts"])
        bank_app.perform_financial_lifecycle(test_data)
        bank_app.assert_lifecycle_results(test_data)
