from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src import crud, schemas

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Career Application Tracker API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

# related to company functions
@app.post("/companies", response_model=schemas.CompanyResponse)
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db)
):
    if crud.get_company_by_name(db, company.company_name) is not None:
        raise HTTPException(status_code=400, detail="Company already exists")
    
    return crud.create_company(db, company)


@app.get("/companies", response_model=list[schemas.CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)


# related to JobApplication functions
@app.post("/applications", response_model=schemas.JobApplicationResponse)
def create_job_application(
    application: schemas.JobApplicationCreate,
    db: Session = Depends(get_db)
):
    company = crud.get_company_by_id(db, application.company_id)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return crud.create_job_application(db, application)


@app.get("/applications", response_model=list[schemas.JobApplicationResponse])
def get_job_applications(
    company_id: int | None = None,
    source: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_job_applications(
        db,
        company_id=company_id,
        source=source,
        search=search
    )


@app.get("/applications/{application_id}", response_model=schemas.JobApplicationResponse)
def get_job_application_by_id(application_id: int, db: Session = Depends(get_db)):

    result = crud.get_job_application_by_id(db, application_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return result


# related to ApplicationNote functions
@app.post(
    "/applications/{application_id}/notes",
    response_model=schemas.ApplicationNoteResponse
)
def create_application_note(
    application_id: int,
    note: schemas.ApplicationNoteCreate,
    db: Session = Depends(get_db)
):
    application = crud.get_job_application_by_id(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.create_application_note(db, application_id, note)


@app.get(
    "/applications/{application_id}/notes",
    response_model=list[schemas.ApplicationNoteResponse]
)
def get_notes_by_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = crud.get_job_application_by_id(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.get_notes_by_application(db, application_id)


# related to Status functions
@app.post("/statuses", response_model=schemas.StatusResponse)
def create_status(
    status: schemas.StatusCreate,
    db: Session = Depends(get_db)
):
    return crud.create_status(db, status)


@app.get("/statuses", response_model=list[schemas.StatusResponse])
def get_statuses(db: Session = Depends(get_db)):
    return crud.get_statuses(db)


# related to StatusHistory functions
@app.post(
    "/applications/{application_id}/status",
    response_model=schemas.StatusHistoryResponse
)
def create_status_history(
    application_id: int,
    status_history: schemas.StatusHistoryCreate,
    db: Session = Depends(get_db)
):
    application = crud.get_job_application_by_id(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    status = crud.get_status_by_id(db, status_history.status_id)

    if status is None:
        raise HTTPException(status_code=404, detail="Status not found")

    return crud.create_status_history(db, application_id, status_history)


@app.get(
    "/applications/{application_id}/status-history",
    response_model=list[schemas.StatusHistoryResponse]
)
def get_status_history_by_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = crud.get_job_application_by_id(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.get_status_history_by_application(db, application_id)


@app.get("/analytics/source-counts")
def get_source_counts(db: Session = Depends(get_db)):
    return crud.get_source_counts(db)


@app.get("/analytics/company-counts")
def get_company_counts(db: Session = Depends(get_db)):
    return crud.get_company_counts(db)


@app.get("/analytics/status-counts")
def get_status_counts(db: Session = Depends(get_db)):
    return crud.get_status_counts(db)


# related to Skill functions 
@app.post("/skills", response_model=schemas.SkillResponse)
def create_skill(
    skill: schemas.SkillCreate,
    db: Session = Depends(get_db)
):
    if crud.get_skill_by_name(db, skill.skill_name) is not None:
        raise HTTPException(status_code=400, detail="Skill already exists")
    
    return crud.create_skill(db, skill)


@app.get("/skills", response_model=list[schemas.SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return crud.get_skills(db)


@app.post("/applications/{application_id}/skills", response_model=schemas.JobSkillResponse)
def add_skill_to_application(
    application_id: int,
    job_skill: schemas.JobSkillCreate,
    db: Session = Depends(get_db)
):
    application = crud.get_job_application_by_id(db, application_id)
    skill = crud.get_skill_by_id(db, job_skill.skill_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    if crud.check_job_skill_by_id(db, application_id, job_skill.skill_id) is not None:
            raise HTTPException(status_code=400, detail="Skill already added to this application")
    
    return crud.add_skill_to_application(db, application_id, job_skill)


@app.get("/applications/{application_id}/skills", response_model=list[schemas.SkillResponse])
def get_skills_by_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    result = crud.get_job_application_by_id(db, application_id)
        
    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return crud.get_skills_by_application(db, application_id)


@app.get("/analytics/skill-counts")
def get_skill_counts(db: Session = Depends(get_db)):
    return crud.get_skill_counts(db)