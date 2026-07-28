from __future__ import annotations

import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import Page

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from enums.account import PageName
from pages.accounts_page import AccountsPage
from pages.bank_app import BankApp
from pages.bill_pay_page import BillPayPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.send_money_page import SendMoneyPage
from pages.transactions_page import TransactionsPage
from pages.transfer_page import TransferPage
from utils.data_loader import load_test_data

REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


@pytest.fixture(scope="session", autouse=True)
def suite_lifecycle() -> Generator[None, None, None]:
    # Per-test browser state is not initialized here so each run stays independent.
    REPORTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    yield


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    return load_test_data()


@pytest.fixture
def bank_app(page: Page, test_data: dict[str, Any]) -> BankApp:
    base_url = test_data["base_url"]
    pages = {
        PageName.LOGIN.value: LoginPage(page, base_url),
        PageName.DASHBOARD.value: DashboardPage(page, base_url),
        PageName.ACCOUNTS.value: AccountsPage(page, base_url),
        PageName.TRANSFER.value: TransferPage(page, base_url),
        PageName.SEND_MONEY.value: SendMoneyPage(page, base_url),
        PageName.BILL_PAY.value: BillPayPage(page, base_url),
        PageName.TRANSACTIONS.value: TransactionsPage(page, base_url),
    }
    return BankApp(pages)


@pytest.fixture(scope="session")
def browser_context_args() -> dict[str, Any]:
    return {
        "viewport": {"width": 1440, "height": 1000},
        "ignore_https_errors": True,
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    funcargs = getattr(item, "funcargs", {})
    page = funcargs.get("page")
    if page is None:
        return

    screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    allure.attach.file(
        str(screenshot_path),
        name=f"{item.name} failure screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
