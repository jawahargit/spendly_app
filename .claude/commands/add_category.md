Add a new expense category to Spendly.

The user will provide the new category name as an argument (e.g. `/add_category Rent`).

Steps:
1. Read `app.py` and locate the `CATEGORIES` list — it appears in **both** `add_expense` and `edit_expense` route functions.
2. Add the new category to both lists, keeping alphabetical order within the custom entries (place it before "Other", which should always be last).
3. Show the user the two updated `CATEGORIES` lines and confirm the change is consistent across both routes.
4. Remind the user that existing expenses with old categories are unaffected — the category is only used in the form dropdowns.
