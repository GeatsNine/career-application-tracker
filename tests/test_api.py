import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api import app
from src.database import Base, get_db
from src import models  # Needed so SQLAlchemy knows all models


# Use a temporary in-memory test database.
# This does NOT touch your real PostgreSQL career_tracker database.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ---------- Helper functions ----------

def create_company(client, company_name="Test Company", location="Sydney"):
    response = client.post(
        "/companies",
        json={
            "company_name": company_name,
            "location": location,
        },
    )

    assert response.status_code == 200
    return response.json()


def create_application(
    client,
    company_id,
    job_title="Graduate Software Engineer",
    source="LinkedIn",
    job_url="https://example.com/test-job",
    applied_date="2026-07-01",
    salary_range="AUD 80,000 - AUD 95,000",
):
    response = client.post(
        "/applications",
        json={
            "company_id": company_id,
            "job_title": job_title,
            "source": source,
            "job_url": job_url,
            "applied_date": applied_date,
            "salary_range": salary_range,
        },
    )

    assert response.status_code == 200
    return response.json()


def create_status(client, status_category="Applied"):
    response = client.post(
        "/statuses",
        json={
            "status_category": status_category,
        },
    )

    assert response.status_code == 200
    return response.json()


def create_skill(client, skill_name="Python"):
    response = client.post(
        "/skills",
        json={
            "skill_name": skill_name,
        },
    )

    assert response.status_code == 200
    return response.json()


# ---------- Basic routes ----------

def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Career Application Tracker API is running"


def test_health_route(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------- Company routes ----------

def test_create_company(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    assert company["id"] == 1
    assert company["company_name"] == "Grab"
    assert company["location"] == "Kuala Lumpur"


def test_get_companies(client):
    create_company(client, "Grab", "Kuala Lumpur")
    create_company(client, "Canva", "Sydney")

    response = client.get("/companies")

    assert response.status_code == 200

    companies = response.json()

    assert len(companies) == 2
    assert companies[0]["company_name"] == "Grab"
    assert companies[1]["company_name"] == "Canva"


# ---------- Job application routes ----------

def test_create_application(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application = create_application(
        client,
        company_id=company["id"],
        job_title="Graduate Software Engineer",
        source="LinkedIn",
        job_url="https://example.com/grab-grad-software",
    )

    assert application["id"] == 1
    assert application["company_id"] == company["id"]
    assert application["job_title"] == "Graduate Software Engineer"
    assert application["source"] == "LinkedIn"


def test_create_application_invalid_company_returns_404(client):
    response = client.post(
        "/applications",
        json={
            "company_id": 999,
            "job_title": "Backend Developer",
            "source": "LinkedIn",
            "job_url": "https://example.com/invalid-company-job",
            "applied_date": "2026-07-01",
            "salary_range": "RM 4,000 - RM 6,000",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"


def test_get_application_by_id(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application = create_application(
        client,
        company_id=company["id"],
        job_title="Backend Developer",
        source="Company Website",
        job_url="https://example.com/backend-developer",
    )

    response = client.get(f"/applications/{application['id']}")

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == application["id"]
    assert result["job_title"] == "Backend Developer"


def test_get_application_by_invalid_id_returns_404(client):
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_get_applications_filters(client):
    grab = create_company(client, "Grab", "Kuala Lumpur")
    canva = create_company(client, "Canva", "Sydney")

    create_application(
        client,
        company_id=grab["id"],
        job_title="Graduate Software Engineer",
        source="LinkedIn",
        job_url="https://example.com/grab-software",
    )

    create_application(
        client,
        company_id=grab["id"],
        job_title="Backend Developer",
        source="Company Website",
        job_url="https://example.com/grab-backend",
    )

    create_application(
        client,
        company_id=canva["id"],
        job_title="Frontend Developer",
        source="LinkedIn",
        job_url="https://example.com/canva-frontend",
    )

    company_response = client.get(f"/applications?company_id={grab['id']}")
    assert company_response.status_code == 200
    assert len(company_response.json()) == 2

    source_response = client.get("/applications?source=LinkedIn")
    assert source_response.status_code == 200
    assert len(source_response.json()) == 2

    search_response = client.get("/applications?search=backend")
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["job_title"] == "Backend Developer"


# ---------- Notes routes ----------

def test_create_and_get_application_notes(client):
    company = create_company(client, "Grab", "Kuala Lumpur")
    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/note-test-job",
    )

    response = client.post(
        f"/applications/{application['id']}/notes",
        json={
            "note_details": "Prepare API and SQL questions.",
            "note_date": "2026-07-02",
        },
    )

    assert response.status_code == 200
    assert response.json()["note_details"] == "Prepare API and SQL questions."

    get_response = client.get(f"/applications/{application['id']}/notes")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    assert get_response.json()[0]["note_details"] == "Prepare API and SQL questions."


def test_create_note_invalid_application_returns_404(client):
    response = client.post(
        "/applications/999/notes",
        json={
            "note_details": "This should fail.",
            "note_date": "2026-07-02",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


# ---------- Status routes ----------

def test_create_and_get_statuses(client):
    create_status(client, "Applied")
    create_status(client, "Interview")

    response = client.get("/statuses")

    assert response.status_code == 200

    statuses = response.json()

    assert len(statuses) == 2
    assert statuses[0]["status_category"] == "Applied"
    assert statuses[1]["status_category"] == "Interview"


def test_create_and_get_status_history(client):
    company = create_company(client, "Grab", "Kuala Lumpur")
    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/status-test-job",
    )
    status = create_status(client, "Applied")

    response = client.post(
        f"/applications/{application['id']}/status",
        json={
            "status_id": status["id"],
            "status_date": "2026-07-03",
        },
    )

    assert response.status_code == 200
    assert response.json()["job_id"] == application["id"]
    assert response.json()["status_id"] == status["id"]

    get_response = client.get(f"/applications/{application['id']}/status-history")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1


def test_create_status_history_invalid_status_returns_404(client):
    company = create_company(client, "Grab", "Kuala Lumpur")
    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/invalid-status-test-job",
    )

    response = client.post(
        f"/applications/{application['id']}/status",
        json={
            "status_id": 999,
            "status_date": "2026-07-03",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Status not found"


# ---------- Analytics routes ----------

def test_source_and_company_analytics(client):
    grab = create_company(client, "Grab", "Kuala Lumpur")
    canva = create_company(client, "Canva", "Sydney")

    create_application(
        client,
        company_id=grab["id"],
        job_title="Software Engineer",
        source="LinkedIn",
        job_url="https://example.com/analytics-job-1",
    )

    create_application(
        client,
        company_id=grab["id"],
        job_title="Backend Developer",
        source="LinkedIn",
        job_url="https://example.com/analytics-job-2",
    )

    create_application(
        client,
        company_id=canva["id"],
        job_title="Frontend Developer",
        source="Company Website",
        job_url="https://example.com/analytics-job-3",
    )

    source_response = client.get("/analytics/source-counts")
    assert source_response.status_code == 200

    source_counts = source_response.json()

    assert source_counts["LinkedIn"] == 2
    assert source_counts["Company Website"] == 1

    company_response = client.get("/analytics/company-counts")
    assert company_response.status_code == 200

    company_counts = company_response.json()

    assert company_counts[str(grab["id"])] == 2
    assert company_counts[str(canva["id"])] == 1


def test_status_analytics(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application_1 = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/status-analytics-1",
    )

    application_2 = create_application(
        client,
        company_id=company["id"],
        job_title="Backend Developer",
        job_url="https://example.com/status-analytics-2",
    )

    applied = create_status(client, "Applied")
    interview = create_status(client, "Interview")

    client.post(
        f"/applications/{application_1['id']}/status",
        json={
            "status_id": applied["id"],
            "status_date": "2026-07-03",
        },
    )

    client.post(
        f"/applications/{application_2['id']}/status",
        json={
            "status_id": applied["id"],
            "status_date": "2026-07-04",
        },
    )

    client.post(
        f"/applications/{application_2['id']}/status",
        json={
            "status_id": interview["id"],
            "status_date": "2026-07-05",
        },
    )

    response = client.get("/analytics/status-counts")

    assert response.status_code == 200

    status_counts = response.json()

    assert status_counts["Applied"] == 2
    assert status_counts["Interview"] == 1


# ---------- Skill routes ----------

def test_create_and_get_skills(client):
    create_skill(client, "Python")
    create_skill(client, "SQL")

    response = client.get("/skills")

    assert response.status_code == 200

    skills = response.json()

    assert len(skills) == 2
    assert skills[0]["skill_name"] == "Python"
    assert skills[1]["skill_name"] == "SQL"


def test_add_and_get_skills_by_application(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/skills-test-job",
    )

    python_skill = create_skill(client, "Python")
    sql_skill = create_skill(client, "SQL")

    response_1 = client.post(
        f"/applications/{application['id']}/skills",
        json={
            "skill_id": python_skill["id"],
        },
    )

    assert response_1.status_code == 200
    assert response_1.json()["job_id"] == application["id"]
    assert response_1.json()["skill_id"] == python_skill["id"]

    response_2 = client.post(
        f"/applications/{application['id']}/skills",
        json={
            "skill_id": sql_skill["id"],
        },
    )

    assert response_2.status_code == 200

    get_response = client.get(f"/applications/{application['id']}/skills")

    assert get_response.status_code == 200

    skills = get_response.json()
    skill_names = [skill["skill_name"] for skill in skills]

    assert "Python" in skill_names
    assert "SQL" in skill_names


def test_add_skill_invalid_application_returns_404(client):
    skill = create_skill(client, "Python")

    response = client.post(
        "/applications/999/skills",
        json={
            "skill_id": skill["id"],
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_add_skill_invalid_skill_returns_404(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/invalid-skill-test-job",
    )

    response = client.post(
        f"/applications/{application['id']}/skills",
        json={
            "skill_id": 999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"


def test_skill_analytics(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application_1 = create_application(
        client,
        company_id=company["id"],
        job_title="Software Engineer",
        job_url="https://example.com/skill-analytics-1",
    )

    application_2 = create_application(
        client,
        company_id=company["id"],
        job_title="Backend Developer",
        job_url="https://example.com/skill-analytics-2",
    )

    python_skill = create_skill(client, "Python")
    sql_skill = create_skill(client, "SQL")
    docker_skill = create_skill(client, "Docker")

    client.post(
        f"/applications/{application_1['id']}/skills",
        json={
            "skill_id": python_skill["id"],
        },
    )

    client.post(
        f"/applications/{application_1['id']}/skills",
        json={
            "skill_id": sql_skill["id"],
        },
    )

    client.post(
        f"/applications/{application_2['id']}/skills",
        json={
            "skill_id": python_skill["id"],
        },
    )

    client.post(
        f"/applications/{application_2['id']}/skills",
        json={
            "skill_id": docker_skill["id"],
        },
    )

    response = client.get("/analytics/skill-counts")

    assert response.status_code == 200

    skill_counts = response.json()

    assert skill_counts["Python"] == 2
    assert skill_counts["SQL"] == 1
    assert skill_counts["Docker"] == 1


def test_create_duplicate_company_returns_400(client):
    create_company(client, "Grab", "Kuala Lumpur")

    response = client.post(
        "/companies",
        json={
            "company_name": "grab",
            "location": "Kuala Lumpur",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Company already exists"


def test_create_duplicate_skill_returns_400(client):
    create_skill(client, "Python")

    response = client.post(
        "/skills",
        json={
            "skill_name": "python",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Skill already exists"


def test_add_duplicate_skill_to_application_returns_400(client):
    company = create_company(client, "Grab", "Kuala Lumpur")

    application = create_application(
        client,
        company_id=company["id"],
        job_url="https://example.com/duplicate-skill-link-test",
    )

    skill = create_skill(client, "Python")

    first_response = client.post(
        f"/applications/{application['id']}/skills",
        json={
            "skill_id": skill["id"],
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/applications/{application['id']}/skills",
        json={
            "skill_id": skill["id"],
        },
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Skill already added to this application"
