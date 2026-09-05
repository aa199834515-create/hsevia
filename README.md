# HSEvia

This branch contains a Streamlit-based HSE portal with branding (logo and basic color theme).

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
- The logo is in assets/logo.svg and used as the page icon and header image.
