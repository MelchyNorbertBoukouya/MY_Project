# MY_Project — Deploying to Render

Quick steps to run locally and deploy this Django app to Render.

## Local setup (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1   # PowerShell
# or: venv\Scripts\activate.bat  # cmd.exe
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations and collect static files:

```powershell
python manage.py migrate
python manage.py collectstatic --noinput
```

4. Run the development server:

```powershell
python manage.py runserver
```

## Deploy to Render (recommended)

This project includes a `render.yaml` and `Procfile` to simplify deploys.

1. Push your repo to a Git provider (GitHub/GitLab/Bitbucket) and connect it to Render.

2. In Render, create a new Web Service from the repo or import the `render.yaml`.
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start Command: handled by `Procfile` (`gunicorn world_explorer.wsgi:application`)

3. Render will provision a Postgres database (if using `render.yaml`) and set `DATABASE_URL`.

4. Required environment variables (set in Render Dashboard or `render.yaml`):
   - `SECRET_KEY` — set a strong secret
   - `DEBUG` — set to `False`
   - `ALLOWED_HOSTS` — e.g., `your-app.onrender.com`

5. After deploy, check logs in Render and run `python manage.py migrate` from the web service shell if necessary.

## Notes
- Static files are served by WhiteNoise; `collectstatic` writes to `staticfiles/`.
- If you use Render's Postgres, `DATABASE_URL` will be available and `world_explorer/settings.py` will use it when present.
- For a production-ready setup consider setting up HTTPS, monitoring, and periodic backups for the DB.

If you'd like, I can also:
- create a small PowerShell deploy script that commits, pushes, and opens the Render dashboard,
- or walk through the Render UI step-by-step while you deploy.
