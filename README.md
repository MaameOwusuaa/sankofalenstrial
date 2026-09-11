# SankofaLens

See the past. Understand the story. Experience the culture.

Full-stack heritage and tourism platform prototype for the HACSA@10 Hackathon.

## Stack
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Database: MySQL
- Authentication: JWT + bcrypt
- Roles: user, admin, superuser
- QR: Python qrcode
- Map: Leaflet CDN

## Features included
- Public heritage discovery page
- Heritage sites and detailed stories
- Interactive map
- QR experience endpoint and QR image generation
- User registration/login
- Role-based access control
- Cultural Passport and badges
- Admin content management endpoints/dashboard shell
- Superuser administration endpoints
- Audit logging
- AI Heritage Guide Naa integration placeholder
- Multilingual-ready content fields
- Production-oriented configuration via environment variables
- CORS, password hashing, JWT expiration, validation, database migrations

## Important credentials/placeholders
Copy `.env.example` to `.env` and fill in:
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST
- MYSQL_PORT
- MYSQL_DB
- SECRET_KEY
- OPENAI_API_KEY (optional until Naa is connected)
- MAP_TILE_URL (optional)

Never commit `.env`.

## Run locally

### 1. Create MySQL database
```sql
CREATE DATABASE sankofalens CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Environment
```bash
cp .env.example .env
```

### 3. Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Migrate
```bash
alembic upgrade head
```

### 5. Seed demo data
```bash
python seed.py
```

### 6. Start
```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Demo accounts after seeding
- User: user@sankofalens.local / ChangeMe123!
- Admin: admin@sankofalens.local / ChangeMe123!
- Superuser: superuser@sankofalens.local / ChangeMe123!

Change these passwords before any real deployment.

## HACSA logo
The project references the official HACSA Foundation logo hosted by HACSA's Sankofa Summit site:
https://summit.thehacsa.org/logo.png

Official HACSA website:
https://www.thehacsa.org/

The logo source was verified from HACSA's official web presence on 8 September 2026.

## Production checklist
- Replace all demo passwords.
- Generate a strong random SECRET_KEY.
- Restrict CORS to the production frontend domain.
- Put the API behind HTTPS.
- Use a managed MySQL instance with backups.
- Store AI credentials only in environment/secret management.
- Replace sample heritage records with verified sources and approved cultural content.
- Add moderation/approval workflow before publishing community-generated stories.
- Add real map provider key if using a paid provider.
- Configure email verification, password reset and rate limiting before launch.

## Code organization

The frontend CSS and JavaScript are intentionally split into feature-focused files so the project is easier to maintain and edit. Code throughout the project is formatted with readable line breaks and indentation rather than compressed one-line statements.

CSS modules are located in `static/css/`, while JavaScript modules are located in `static/js/`. Backend Python code is separated into configuration, database, models, schemas, security, routers, and migrations.
