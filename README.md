# HSEvia

This branch contains a simple Streamlit-based HSE portal.

Run locally:

1. Checkout the branch:
   git fetch origin
   git checkout hse-site

2. Install requirements (preferably in a virtualenv):
   pip install -r requirements.txt

3. Set an admin password (used to access the Reports page):
   export STREAMLIT_ADMIN_PASSWORD="yourpassword"
   (Windows PowerShell: $env:STREAMLIT_ADMIN_PASSWORD = "yourpassword")

4. Run the app:
   streamlit run app.py

Notes:
- A SQLite database `hsevia.db` will be created in the repo root on first run.
- Uploaded attachments are saved to the `uploads/` directory (this folder is gitignored).
- Do NOT commit your admin password; set it as an environment variable or use Streamlit secrets in production.
