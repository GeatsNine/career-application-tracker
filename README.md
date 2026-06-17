# Career Application Tracker

A full-stack career application tracking project built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Streamlit**, and **pytest**.

This project helps users track job applications, companies, application notes, status history, required skills, and application analytics in one place.

## Project Overview

When applying for many jobs, it becomes difficult to remember:

* which companies I applied to
* which application came from which source
* what stage each application is in
* what notes I wrote for each role
* what technical skills keep appearing across job posts

This project solves that problem by providing a backend API, relational database, dashboard, analytics, and automated tests.

## Features

### Application Tracking

* Create companies
* Create job applications linked to companies
* View all applications
* Filter applications by company, source, and search keyword
* View a single application by ID

### Notes and Status History

* Add notes to an application
* View notes for an application
* Create application statuses
* Add status history records to an application
* View status history for each application

### Skill Tracking

* Create technical skills
* Link skills to job applications
* View skills required by each application
* Track top required skills across applications

### Analytics

The API and dashboard include analytics for:

* applications by source
* applications by company
* applications by status history
* top required skills

### Error Handling

The API handles common errors clearly, including:

* duplicate company names
* duplicate skill names
* duplicate skill links for the same application
* invalid company IDs
* invalid application IDs
* invalid skill IDs
* invalid status IDs

### Automated Testing

The project includes automated API tests using `pytest` and FastAPI `TestClient`.

The tests cover:

* health check route
* company creation and listing
* application creation and filtering
* invalid application cases
* notes
* statuses
* status history
* analytics
* skills
* duplicate handling

## Tech Stack

| Area                  | Technology                 |
| --------------------- | -------------------------- |
| Backend API           | FastAPI                    |
| Database              | PostgreSQL                 |
| ORM                   | SQLAlchemy                 |
| Dashboard             | Streamlit                  |
| Data Handling         | Pandas                     |
| Testing               | pytest, FastAPI TestClient |
| Environment Variables | python-dotenv              |

## Project Structure

```txt
Career Application Tracker/
├── assets/
│   ├── dashboard_summary.png
│   ├── dashboard_filters.png
│   ├── dashboard_analytics.png
│   ├── api_docs.png
│   └── tests_passed.png
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── crud.py
│   ├── dashboard.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── create_tables.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Dashboard Preview

### Summary Dashboard

![Dashboard Summary](assets/dashboard_summary.png)

### Application Filters

![Dashboard Filters](assets/dashboard_filters.png)

### Analytics Charts

![Dashboard Analytics](assets/dashboard_analytics.png)

## API Documentation

FastAPI automatically provides interactive API documentation.

![API Docs](assets/api_docs.png)

When running locally, open:

```txt
http://127.0.0.1:8000/docs
```

## Database Design Summary

The project uses a relational database structure.

Main tables:

* `companies`
* `job_applications`
* `application_notes`
* `statuses`
* `status_history`
* `skills`
* `job_skills`

Key relationships:

* One company can have many job applications
* One job application can have many notes
* One job application can have many status history records
* One job application can have many skills
* One skill can belong to many job applications

The `job_skills` table is a junction table that supports the many-to-many relationship between job applications and skills.

## Main API Routes

### General

```txt
GET /
GET /health
```

### Companies

```txt
POST /companies
GET /companies
```

### Applications

```txt
POST /applications
GET /applications
GET /applications/{application_id}
```

Supported query filters:

```txt
GET /applications?company_id=1
GET /applications?source=LinkedIn
GET /applications?search=software
```

### Notes

```txt
POST /applications/{application_id}/notes
GET /applications/{application_id}/notes
```

### Statuses

```txt
POST /statuses
GET /statuses
POST /applications/{application_id}/status
GET /applications/{application_id}/status-history
```

### Skills

```txt
POST /skills
GET /skills
POST /applications/{application_id}/skills
GET /applications/{application_id}/skills
```

### Analytics

```txt
GET /analytics/source-counts
GET /analytics/company-counts
GET /analytics/status-counts
GET /analytics/skill-counts
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "Career Application Tracker"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/career_tracker
API_URL=http://127.0.0.1:8000
```

Do not commit your real `.env` file to GitHub.

### 5. Create database tables

```bash
python -m src.create_tables
```

### 6. Run FastAPI backend

```bash
python -m uvicorn src.api:app --reload
```

Backend runs at:

```txt
http://127.0.0.1:8000
```

### 7. Run Streamlit dashboard

Open a second terminal:

```bash
python -m streamlit run src/dashboard.py
```

Dashboard runs at:

```txt
http://localhost:8501
```

## Running Tests

Run all tests:

```bash
python -m pytest -v
```

Example result:

![Tests Passed](assets/tests_passed.png)

## What I Learned

Through this project, I practiced:

* designing relational database models
* using SQLAlchemy relationships
* building FastAPI CRUD routes
* connecting FastAPI with PostgreSQL
* creating many-to-many relationships
* building a Streamlit dashboard
* adding analytics endpoints
* handling API errors properly
* writing automated API tests with pytest
* using environment variables safely

## Future Improvements

Possible future improvements:

* add user authentication
* add resume version tracking
* add follow-up reminder dates
* improve dashboard forms for creating applications
* return company names instead of company IDs in analytics
* return status names directly in status history
* add automatic skill detection from job descriptions
* deploy backend and dashboard online

```
```
