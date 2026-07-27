# Selector Inventory

This file documents the selector strategy used for the Bank QA Playground tests.

## Strategy

- Prefer stable `data-testid` selectors when they exist.
- Use accessible locators (`get_by_role`, `get_by_label`, `get_by_text`) as the main fallback.
- Declare all static locators at the top of each page class (`__init__`) with plain text selectors.
- Action methods use only those locator attributes / dynamic locator helpers.
- Keep all selectors inside `pages/`; tests must not call raw Playwright selectors.
- Use enums in tests and functions for fixed domain values (account names/types, scenario names). Do not wrap enums inside locator definitions.
- Avoid brittle XPath, CSS chains, nth-child selectors, and fixed sleeps.

## Pages Covered

### Login

- Heading: `SecureBank`
- Username: `data-testid=login-username-input`
- Password: `data-testid=login-password-input`
- Submit: role button `Sign In`

### Accounts

- Page heading: `My Accounts`
- Add account: role button `Add Account`
- Account modal: `data-testid=add-account-dialog`
- Account form: `data-testid=account-form`
- Account name: `data-testid=account-form-name-input`
- Account type: `data-testid=account-form-type-select`
- Starting balance: `input[name='account_balance_field']`
- Accept terms: `data-testid=account-form-accept-terms-checkbox`
- Save: `data-testid=save-account-form-btn`

### Transfer

- Page heading: `Transfer Money`
- Form: `data-testid=transfer-form`
- From account: `data-testid=transfer-from-select`
- To account: `data-testid=transfer-to-select`
- Amount: `data-testid=transfer-amount-input`
- Memo: placeholder `e.g. Rent, vacation fund...`
- Review: `data-testid=review-transfer-btn`

### Send Money

- Page heading: `Send Money`
- Payee select: `data-testid=payee-select`
- Add payee dialog: `data-testid=add-payee-dialog`
- Payee name: `data-testid=add-payee-name-input`
- Payee bank: `data-testid=add-payee-bank-input`
- Routing number: `data-testid=add-payee-routing-input`
- Account number: `data-testid=add-payee-account-input`
- Save payee: `data-testid=save-add-payee-btn`

### Bill Pay

- Page heading: `Pay a Bill`
- Form: `data-testid=bill-pay-form`
- From account: `data-testid=bill-pay-from-select`
- Add biller: `data-testid=add-biller-btn`
- Add biller dialog: `data-testid=add-biller-dialog`
- Biller name: `data-testid=add-biller-name-input`
- Biller reference: `input[name='biller_ref_field']`
- Save biller: `data-testid=save-add-biller-btn`
- Biller search: `data-testid=biller-search-input`
- Amount: `data-testid=bill-amount-input`
- Memo: `data-testid=bill-memo-input`
- Review: `data-testid=review-bill-btn`

### Transactions

- Page heading: `Transactions`
- Transaction verification is by configured memo/note text and formatted amount.

## Live App Note

The Bank Demo app has changed over time. If a current live selector differs, update the page object only. Test files should remain unchanged.
