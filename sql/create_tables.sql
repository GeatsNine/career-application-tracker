DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS job_status;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS job_applications;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies(
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    location TEXT NOT NULL
);


CREATE TABLE job_applications(
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    source TEXT NOT NULL,
    job_url TEXT UNIQUE,
    applied_date DATE,
    salary_range TEXT,
    created_at DATE DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(company_id) REFERENCES companies(id)
);


CREATE TABLE statuses(
    id SERIAL PRIMARY KEY,
    status_category TEXT NOT NULL UNIQUE
);


CREATE TABLE job_status(
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    status_date DATE NOT NULL,
    FOREIGN KEY(job_id) REFERENCES job_applications(id),
    FOREIGN KEY(status_id) REFERENCES statuses(id)
);


CREATE TABLE notes(
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    note_details TEXT NOT NULL,
    note_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY(job_id) REFERENCES job_applications(id)
);


CREATE TABLE skills(
    id SERIAL PRIMARY KEY,
    skill_name TEXT NOT NULL UNIQUE
);


CREATE TABLE job_skills(
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    FOREIGN KEY(job_id) REFERENCES job_applications(id),
    FOREIGN KEY(skill_id) REFERENCES skills(id),
    -- UNIQUE(job_id, skill_id)
);
