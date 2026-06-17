from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base


class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)

    job_applications = relationship("JobApplication", back_populates="company")
    # One Company can have many JobApplication records.


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    job_title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    job_url = Column(String, nullable=True, unique=True)
    applied_date = Column(Date, nullable=True)
    salary_range = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="job_applications")
    # Each JobApplication belongs to one Company.

    notes = relationship("ApplicationNote", back_populates="job_application")
    # One JobApplication can have many ApplicationNote records.

    status_history = relationship("StatusHistory", back_populates="job_application")
    # One JobApplication can have many StatusHistory records.

    job_skills = relationship("JobSkill", back_populates="job_application")
    # One JobApplication can have many JobSkill records.


class ApplicationNote(Base):
    __tablename__ = "application_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    note_details = Column(Text, nullable=False)
    note_date = Column(Date, nullable=True)

    job_application = relationship("JobApplication", back_populates="notes")
    # Each ApplicationNote belongs to one JobApplication.


class Status(Base):
    __tablename__ = "statuses"
        
    id = Column(Integer, primary_key=True, index=True)
    status_category = Column(String, nullable=False, unique=True)

    status_history = relationship("StatusHistory", back_populates="status")
    # One Status can be used in many StatusHistory records.

class StatusHistory(Base):
    __tablename__ = "status_history"
        
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    status_date = Column(Date, nullable=False)

    job_application  = relationship("JobApplication", back_populates="status_history")
    # Each StatusHistory belongs to one JobApplication.

    status = relationship("Status", back_populates="status_history")
    # Each StatusHistory record uses one Status.


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, unique=True)

    job_skills = relationship("JobSkill", back_populates="skill")
    # One Skill can appear in many JobSkill records.

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    skill = relationship("Skill", back_populates="job_skills")
    # JobSkill belongs to one Skill

    job_application = relationship("JobApplication", back_populates="job_skills")
    # JobSkill belongs to one JobApplication