# TalentLedger Backend

A RESTful API built with Django and Django Rest Framework to manage talent skills and transactions.

## Features
- **CRUD Operations**: Complete management of skills.
- **RESTful API**: Clean JSON responses for seamless frontend integration.
- **Data Integrity**: Relational database modeling with user-to-skill mapping.

## Setup Instructions
1. Clone the repository: `git clone <your-repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## API Endpoints
- `GET /api/skills/`: List all skills
- `POST /api/skills/`: Create a new skill
- `PUT /api/skills/<id>/`: Update a skill
- `DELETE /api/skills/<id>/`: Delete a skill
