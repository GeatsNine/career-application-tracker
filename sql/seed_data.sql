-- Seed statuses
INSERT INTO statuses (status_category) VALUES
('Saved'),
('Applied'),
('Online Assessment'),
('Interview'),
('Offer'),
('Rejected'),
('Ghosted'),
('Withdrawn');

-- Seed companies
INSERT INTO companies (company_name, location) VALUES
('Grab', 'Kuala Lumpur'),
('AirAsia', 'Kuala Lumpur');

-- Seed skills
INSERT INTO skills (skill_name) VALUES
('Python'),
('SQL'),
('Git'),
('REST API'),
('Java'),
('Spring Boot'),
('PostgreSQL');

-- Seed job applications
INSERT INTO job_applications (
    company_id,
    job_title,
    source,
    job_url,
    applied_date,
    salary_range
) VALUES
(
    1,
    'Graduate Software Engineer',
    'LinkedIn',
    'https://example.com/grab-grad-software-engineer',
    '2026-07-01',
    'RM 4,000 - RM 6,000'
),
(
    2,
    'Junior Backend Developer',
    'Company Website',
    'https://example.com/airasia-backend-developer',
    '2026-07-03',
    'RM 4,500 - RM 6,500'
);

-- Seed job status history
-- status_id 2 = Applied
-- status_id 3 = Online Assessment
INSERT INTO job_status (job_id, status_id, status_date) VALUES
(1, 2, '2026-07-01'),
(2, 3, '2026-07-06');

-- Seed notes
INSERT INTO notes (job_id, note_details, note_date) VALUES
(1, 'Need to follow up if no response after two weeks.', '2026-07-02'),
(2, 'Prepare API and database questions.', '2026-07-06');

-- Seed job skills
-- Job 1: Python, SQL, Git, REST API
-- Job 2: Java, Spring Boot, SQL, PostgreSQL
INSERT INTO job_skills (job_id, skill_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 5),
(2, 6),
(2, 2),
(2, 7);

select * from companies;        -- 2 companies
select * from job_applications; -- 2 jobs
select * from statuses;         -- 8 statuses
select * from skills;           -- 7 skills
select * from notes;            -- 2 notes
select * from job_status;       -- 2 job status records
select * from job_skills;       -- 7 job-skill records