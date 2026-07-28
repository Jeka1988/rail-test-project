# Bank QA Playground Automation

Python + Playwright automation project for the Bank QA Playground home exercise.

## What This Covers

The suite contains three `@pytest.mark.e2e` scenarios:

1. **Account lifecycle (happy path)** — clean session, login, create Checking/Savings, transfer + send money + bill pay, then verify balances, net worth, and transaction history.
2. **Login negative** — wrong password stays on the login page with an error message.
3. **Transfer negative** — overdraft transfer is rejected; balances, net worth, and history stay unchanged.

## Tech Stack

- Python
- Playwright
- pytest
- pytest-playwright
- pytest-html
- allure-pytest

## Project Structure

```text
config/                 Test data and configurable values
docs/                   Selector inventory and notes
pages/                  Page Object Model and BankApp facade
tests/                  Thin pytest tests
utils/                  Shared data and money helpers
reports/                Generated reports, screenshots, and Allure output
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
playwright install chromium
```

In Cursor/VS Code, select the interpreter:

`${workspaceFolder}/.venv/bin/python`

Then reload the window so Go to Definition works for `pages.*` imports.

Optional local overrides:

```bash
cp .env.example .env
```

Every E2E field in `config/test_data.yaml` can be overridden via environment variables (see `.env.example`). Account names and types are plain strings, so alternate values work without editing enums.

Inline override examples:

```bash
BANK_USERNAME=overdraft_user BANK_PASSWORD=bank_sauce TRANSFER_AMOUNT=50 pytest -m e2e
```

```bash
TEST_DATA_PATH=config/test_data.yaml pytest -m e2e
```

Useful overrides include credentials (`BANK_USERNAME`, `BANK_PASSWORD`), accounts (`CHECKING_ACCOUNT_NAME`, `SAVINGS_ACCOUNT_TYPE`, …), transfer (`TRANSFER_FROM`, `TRANSFER_AMOUNT`, …), send money (`SEND_AMOUNT`, `PAYEE_NAME`, …), and bill pay (`BILL_AMOUNT`, `BILLER_NAME`, …). Set `TEST_DATA_PATH` to swap the full YAML file.

## Run Tests

```bash
pytest
```

Run headed:

```bash
pytest --headed
```

Run all E2E scenarios:

```bash
pytest -m e2e
```

Run one file:

```bash
pytest tests/test_account_lifecycle_e2e.py
pytest tests/test_login_negative.py
pytest tests/test_transfer_negative.py
```

## Reports

- HTML report: `reports/report.html`
- Allure results: `reports/allure`
- Failure screenshots: `reports/screenshots`
- Playwright traces: retained on failure through pytest-playwright

To view Allure results, install the Allure CLI and run:

```bash
allure serve reports/allure
```

## Playwright Best Practices Used

- Strict Page Object Model.
- Tests call only page/facade business methods.
- No raw locators, clicks, fills, or waits inside test files.
- Prefer `data-testid` and accessible locators.
- Use Playwright web-first assertions instead of fixed sleeps.
- Fresh browser context and storage reset for independent reruns.
- Failure artifacts for debugging.

## Python Equivalents For Playwright Test Concepts

The assignment requires Python, so the suite uses pytest equivalents:

- `class TestAccountLifecycle` / `TestLoginNegative` / `TestTransferNegative` group tests like `test.describe`.
- `suite_lifecycle` fixture with `yield` acts as before-all/after-all setup and cleanup.
- Function-scoped fixtures keep each test independent.

## Requirements Coverage

- Python + Playwright: implemented with `pytest-playwright`.
- Modern automation architecture: implemented with POM and a `BankApp` facade.
- Separation between test and UI logic: tests only call page/facade methods.
- Stable reruns: storage reset and fresh browser context.
- Dynamic UI handling: Playwright assertions and bounded waits.
- Parameterization: data lives in `config/test_data.yaml` and is fully overridable via env vars or `TEST_DATA_PATH`.
- Reporting: pytest-html, Allure steps, screenshots, and traces.
- README: setup, first run, and execution commands are documented here.

## Deposit / Current Account Note

The current Bank Demo UI may not expose a dedicated deposit or salary operation. If it does during implementation, it should be included in the lifecycle. Otherwise, the test uses opening balances plus transfer, send money, and bill pay as the available account-changing operations and verifies the final state precisely.
