from sqlalchemy.orm import Session
from sqlalchemy import func
from src import models, schemas


# related to company functions
def get_company_by_name(db: Session, company_name: str):
    cleaned_company_name = company_name.strip().lower()

    return (
        db.query(models.Company)
        .filter(func.lower(models.Company.company_name) == cleaned_company_name)
        .first()
        )

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(
        company_name=company.company_name.strip(),
        location=company.location
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def get_companies(db: Session):
    return db.query(models.Company).all()


def get_company_by_id(db: Session, company_id: int):
    return (
        db.query(models.Company)
        .filter(models.Company.id == company_id)
        .first()
    )


# related to JobApplication functions
def create_job_application(db: Session, application: schemas.JobApplicationCreate):
    db_job_application = models.JobApplication(
        company_id=application.company_id,
        job_title=application.job_title,
        source=application.source,
        job_url=application.job_url,
        applied_date=application.applied_date,
        salary_range=application.salary_range
    )

    db.add(db_job_application)
    db.commit()
    db.refresh(db_job_application)

    return db_job_application


def get_job_applications(
    db: Session,
    company_id: int | None = None,
    source: str | None = None,
    search: str | None = None
):
    query =  db.query(models.JobApplication)

    if company_id is not None:
        query = query.filter(models.JobApplication.company_id == company_id)

    if source is not None:
        query = query.filter(models.JobApplication.source == source)

    if search is not None:
        query = query.filter(models.JobApplication.job_title.ilike(f"%{search}%"))

    return query.all()


def get_job_application_by_id(db: Session, application_id: int):
    return (
            db.query(models.JobApplication)
            .filter(models.JobApplication.id == application_id)
            .first()
        )


# related to ApplicationNote functions
def create_application_note(
    db: Session,
    application_id: int,
    note: schemas.ApplicationNoteCreate
):
    db_note = models.ApplicationNote(
        job_id=application_id,
        note_details=note.note_details,
        note_date=note.note_date
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def get_notes_by_application(db: Session, application_id: int):
    return (
        db.query(models.ApplicationNote)
        .filter(models.ApplicationNote.job_id == application_id)
        .all()
    )


# related to Status functions
def create_status(db: Session, status: schemas.StatusCreate):
    db_status = models.Status(
        status_category=status.status_category
    )

    db.add(db_status)
    db.commit()
    db.refresh(db_status)

    return db_status


def get_statuses(db: Session):
    return db.query(models.Status).all()


def get_status_by_id(db: Session, status_id: int):
    return (
        db.query(models.Status)
        .filter(models.Status.id == status_id)
        .first()
    )


# related to StatusHistory functions
def create_status_history(
    db: Session,
    application_id: int,
    status_history: schemas.StatusHistoryCreate
):
    db_status_history = models.StatusHistory(
        job_id=application_id,
        status_id=status_history.status_id,
        status_date=status_history.status_date
    )

    db.add(db_status_history)
    db.commit()
    db.refresh(db_status_history)

    return db_status_history


def get_status_history_by_application(db: Session, application_id: int):
    return (
        db.query(models.StatusHistory)
        .filter(models.StatusHistory.job_id == application_id)
        .all()
    )

# .all()   → returns a list, maybe []
# .first() → returns one object or None


# related to count function
def get_source_counts(db: Session):
    rows = (
        db.query(
            models.JobApplication.source,
            func.count(models.JobApplication.id)
        )
        .group_by(models.JobApplication.source)
        .all()
    )

    result = {}

    for source, count in rows:
        result[source] = count

    return result


def get_company_counts(db: Session):
    rows = (
        db.query(
            models.JobApplication.company_id,
            func.count(models.JobApplication.id)
        )
        .group_by(models.JobApplication.company_id)
        .all()
    )

    result = {}

    for company_id, count in rows:
        result[company_id] = count

    return result


def get_status_counts(db: Session):
    rows = (
        db.query(
            models.Status.status_category,
            func.count(models.StatusHistory.id)
        )
        .join(models.StatusHistory, models.Status.id == models.StatusHistory.status_id)
        .group_by(models.Status.status_category)
        .all()
    )

    result = {}

    for status_category, count in rows:
        result[status_category] = count

    return result


# related to Skill functions
def get_skill_by_name(db: Session, skill_name: str):
    cleaned_skill_name = skill_name.strip().lower()

    return (
        db.query(models.Skill)
        .filter(func.lower(models.Skill.skill_name) == cleaned_skill_name)
        .first()
        )

def create_skill(db: Session, skill: schemas.SkillCreate):
    db_skill = models.Skill(
        skill_name=skill.skill_name.strip()
    )

    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill


def get_skills(db: Session):
    return db.query(models.Skill).all()


def get_skill_by_id(db: Session, skill_id: int):
    return (
        db.query(models.Skill)
        .filter(models.Skill.id == skill_id)
        .first()
    )


def check_job_skill_by_id(db: Session, application_id: int, skill_id: int):
    return (
        db.query(models.JobSkill)
        .filter(
            models.JobSkill.job_id == application_id, 
            models.JobSkill.skill_id == skill_id
            )
        .first()
    )


def add_skill_to_application(db: Session, application_id: int, job_skill: schemas.JobSkillCreate):
    db_job_skill = models.JobSkill(
        job_id=application_id, 
        skill_id=job_skill.skill_id
    )
    
    db.add(db_job_skill)
    db.commit()
    db.refresh(db_job_skill)

    return db_job_skill


def get_skills_by_application(db: Session, application_id: int):
    return (
        db.query(models.Skill)
        .join(models.JobSkill, models.Skill.id == models.JobSkill.skill_id)
        .filter(models.JobSkill.job_id == application_id)
        .all()
    )


def get_skill_counts(db: Session):
    rows = (
        db.query(
            models.Skill.skill_name,
            func.count(models.JobSkill.skill_id)
        )
        .join(models.JobSkill, models.Skill.id == models.JobSkill.skill_id)
        .group_by(models.Skill.skill_name)
        .all()
    )

    result = {}

    for skill_name, count in rows:
        result[skill_name] = count

    return result