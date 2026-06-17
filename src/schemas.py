from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


# Company schemas
class CompanyBase(BaseModel):
    company_name: str
    location: str


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Job application schemas
class JobApplicationBase(BaseModel):
    company_id: int
    job_title: str
    source: str
    job_url: str | None = None
    applied_date: date | None = None
    salary_range: str | None = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationUpdate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Application note schemas
class ApplicationNoteBase(BaseModel):
    note_details: str
    note_date: date | None = None


class ApplicationNoteCreate(ApplicationNoteBase):
    pass


class ApplicationNoteResponse(ApplicationNoteBase):
    id: int
    job_id: int

    model_config = ConfigDict(from_attributes=True)


# Status schemas
class StatusBase(BaseModel):
    status_category: str


class StatusCreate(StatusBase):
    pass


class StatusResponse(StatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Status history schemas
class StatusHistoryBase(BaseModel):
    status_id: int
    status_date: date


class StatusHistoryCreate(StatusHistoryBase):
    pass


class StatusHistoryResponse(StatusHistoryBase):
    id: int
    job_id: int

    model_config = ConfigDict(from_attributes=True)


# Skill schemas
class SkillBase(BaseModel):
    skill_name: str


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


# JobSkill schemas
class JobSkillBase(BaseModel):
    skill_id: int


class JobSkillCreate(JobSkillBase):
    pass


class JobSkillResponse(JobSkillBase):
    id: int
    job_id: int
    
    model_config = ConfigDict(from_attributes=True)


