# TalentLedger

TalentLedger is a peer-to-peer skill-exchange and study-credit platform built with **Django** and **Django REST Framework (DRF)**, deployed on **Render**. Learners and instructors exchange expertise using study credits rather than cash payments.

## Live App
- **Production URL:** [https://talentledgerproject.onrender.com/](https://talentledgerproject.onrender.com/)

## Key Features
- **Authentication & Profiles:** User registration and login with starting study credits and Discord handle support.
- **Skill Marketplace & Management:** Browse available skills, publish new skills linked to an instructor, and delete skills you created.
- **Session Booking & Credit Escrow:** Book sessions with instructors, hold credits in escrow upon booking confirmation, and view incoming requests or personal bookings.
- **Session Completion & Credit Award:** Complete sessions and trigger `/api/transactions/<id>/award-credit/` to release credit to the instructor.
- **Subscriptions:** Dedicated `/subscription/` page accessible directly from the navigation bar.

## Tech Stack
- **Backend & API:** Python, Django, Django REST Framework (`CsrfExemptSessionAuthentication` for session-backed API requests)
- **Frontend:** Django Templates, HTML, CSS, JavaScript
- **Database & Hosting:** PostgreSQL, Render

## Core API Endpoints
- `POST /api/auth/signup/` — Register a new user
- `POST /api/auth/login/` — Authenticate a user session
- `GET /api/users/` — List users and credit balances
- `GET / POST /api/skills/` — List or create skills
- `GET / DELETE /api/skills/<id>/` — Retrieve or delete a skill
- `POST /api/skills/<skill_id>/book/` — Book a skill session
- `GET /api/instructor/requests/` — View incoming booking requests for an instructor
- `GET /api/my-bookings/` — View a user's booked sessions
- `POST /api/transactions/<transaction_id>/respond/` — Accept, deny, or schedule a booking
- `POST /api/transactions/<id>/award-credit/` — Complete a session and award credit to the instructor

## Local Setup
1. Clone the repository and enter the project directory:
```bash
git clone <your-repo-url>
cd TalentLedger
```
2. Create and activate a virtual environment, then install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run migrations and start the development server:
```bash
python manage.py migrate
python manage.py runserver
```

## Roadmap / Future Improvements
- Automated credit refunds on cancelled bookings
- Post-session peer ratings and reviews
- Deeper Discord integration for session tracking