Reset and reseed the Spendly database with sample data.

Steps:
1. Delete `database/spendly.db` if it exists.
2. Run `venv/bin/python database/db.py` to recreate the schema and insert seed data.
3. Confirm success and remind the user that sample login credentials are `nitish@example.com` / `password123`.
