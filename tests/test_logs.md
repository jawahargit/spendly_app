# Spendly — Test Run Log

**Run date:** 2026-06-14 19:50:05  

---

## ✅ `tests/test_auth.py::TestRegister::test_register_success_redirects_to_dashboard`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestRegister::test_register_sets_session`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestRegister::test_register_duplicate_email_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Create account — Spendly
error → An account with that email already exists.
```

---

## ✅ `tests/test_auth.py::TestRegister::test_register_missing_name_shows_error`

```text
POST  /register
data  → {'name': '', 'email': 'x@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Create account — Spendly
error → All fields are required.
```

---

## ✅ `tests/test_auth.py::TestRegister::test_register_missing_email_shows_error`

```text
POST  /register
data  → {'name': 'Bob', 'email': '', 'password': '●●●●●●●●'}
status← 200
page  → Create account — Spendly
error → All fields are required.
```

---

## ✅ `tests/test_auth.py::TestRegister::test_register_short_password_shows_error`

```text
POST  /register
data  → {'name': 'Bob', 'email': 'bob@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Create account — Spendly
error → Password must be at least 8 characters.
```

---

## ✅ `tests/test_auth.py::TestRegister::test_logged_in_user_redirected_away_from_register`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /register
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestLogin::test_login_success_redirects_to_dashboard`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /login
data  → {'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestLogin::test_login_sets_session`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /login
data  → {'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestLogin::test_login_wrong_password_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /login
data  → {'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Sign in — Spendly
error → Invalid email or password.
```

---

## ✅ `tests/test_auth.py::TestLogin::test_login_unknown_email_shows_same_error`

```text
POST  /login
data  → {'email': 'nobody@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Sign in — Spendly
error → Invalid email or password.
```

---

## ✅ `tests/test_auth.py::TestLogin::test_login_missing_fields_shows_error`

```text
POST  /login
data  → {'email': '', 'password': '●●●●●●●●'}
status← 200
page  → Sign in — Spendly
error → Email and password are required.
```

---

## ✅ `tests/test_auth.py::TestLogin::test_logged_in_user_redirected_away_from_login`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /login
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_auth.py::TestLogout::test_logout_clears_session`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

---

## ✅ `tests/test_auth.py::TestLogout::test_logout_redirects_to_landing`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

---

## ✅ `tests/test_auth.py::TestLogout::test_protected_route_after_logout_redirects_to_login`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
GET   /dashboard
status← 200
page  → Sign in — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_requires_login`

```text
GET   /dashboard
status← 200
page  → Sign in — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_loads_for_logged_in_user`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_shows_user_greeting`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_empty_state_shows_zero_totals`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_shows_added_expense_in_recent_list`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Lunch', 'amount': '200', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_transaction_count_increments`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Expense One', 'amount': '100', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Expense Two', 'amount': '200', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Expense Three', 'amount': '300', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_only_shows_own_expenses`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Alice Expense', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /register
data  → {'name': 'Bob', 'email': 'bob@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_category_chart_data_present`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '500', 'category': 'Transport', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_dashboard.py::TestDashboard::test_dashboard_add_expense_link_present`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_requires_login`

```text
GET   /expenses/add
status← 200
page  → Sign in — Spendly
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_success_redirects_to_dashboard`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_missing_title_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': '', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Add Expense — Spendly
error → Title is required.
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_missing_amount_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Add Expense — Spendly
error → Amount is required.
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_zero_amount_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '0', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Add Expense — Spendly
error → Amount must be a positive number.
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_negative_amount_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '-50', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Add Expense — Spendly
error → Amount must be a positive number.
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_missing_date_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '', 'note': ''}
status← 200
page  → Add Expense — Spendly
error → Date is required.
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_form_preloads_today`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /expenses/add
status← 200
page  → Add Expense — Spendly
```

---

## ✅ `tests/test_expenses.py::TestAddExpense::test_add_get_shows_category_dropdown`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /expenses/add
status← 200
page  → Add Expense — Spendly
```

---

## ✅ `tests/test_expenses.py::TestEditExpense::test_edit_success_updates_record`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/1/edit
data  → {'title': 'Latte', 'amount': '150', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestEditExpense::test_edit_missing_title_shows_error`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/1/edit
data  → {'title': '', 'amount': '150', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Edit Expense — Spendly
error → Title is required.
```

---

## ✅ `tests/test_expenses.py::TestEditExpense::test_edit_prefills_existing_values`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
GET   /expenses/1/edit
status← 200
page  → Edit Expense — Spendly
```

---

## ✅ `tests/test_expenses.py::TestEditExpense::test_edit_another_users_expense_redirects`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /register
data  → {'name': 'Bob', 'email': 'bob@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/2/edit
data  → {'title': 'Hacked', 'amount': '1', 'category': 'Other', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestEditExpense::test_edit_requires_login`

```text
GET   /expenses/999/edit
status← 200
page  → Sign in — Spendly
```

---

## ✅ `tests/test_expenses.py::TestDeleteExpense::test_delete_removes_expense_from_dashboard`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/1/delete
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestDeleteExpense::test_delete_another_users_expense_has_no_effect`

```text
POST  /register
data  → {'name': 'Alice', 'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/add
data  → {'title': 'Coffee', 'amount': '120', 'category': 'Food', 'date': '2026-06-14', 'note': ''}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /register
data  → {'name': 'Bob', 'email': 'bob@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
POST  /expenses/1/delete
status← 200
page  → Dashboard — Spendly
```

```text
GET   /logout
status← 200
page  → Spendly — Track Every Rupee
```

```text
POST  /login
data  → {'email': 'alice@example.com', 'password': '●●●●●●●●'}
status← 200
page  → Dashboard — Spendly
```

```text
GET   /dashboard
status← 200
page  → Dashboard — Spendly
```

---

## ✅ `tests/test_expenses.py::TestDeleteExpense::test_delete_requires_login`

```text
POST  /expenses/999/delete
status← 200
page  → Sign in — Spendly
```

---

## Summary

| Result | Count |
| --- | --- |
| **Total** | 42 |
| ✅ Passed | 42 |
| ❌ Failed | 0 |
