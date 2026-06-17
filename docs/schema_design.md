# Career Application Tracker - Database Schema Design

## Project Problem

When applying for jobs, it is easy to lose track of companies, job applications, statuses, notes, required skills, and follow-up progress.

This project solves that problem by storing job applications in a structured database. The app will help users track where they applied, what stage each application is in, what skills each job requires, and any notes related to each application.

## Main Entities

The main entities in this system are:

1. Companies
2. Job Applications
3. Statuses
4. Job Status History
5. Notes
6. Skills
7. Job Skills

---

## Entity 1: Companies

The `companies` table stores company information.

| Column       | Data Type | Constraint                | Description               |
| ------------ | --------- | ------------------------- | ------------------------- |
| id           | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique company ID         |
| company_name | TEXT      | NOT NULL, UNIQUE          | Name of the company       |
| location     | TEXT      | NOT NULL                  | Main job/company location |

### Example

| id | company_name | location     |
| -- | ------------ | ------------ |
| 1  | Grab         | Kuala Lumpur |
| 2  | Canva        | Sydney       |

---

## Entity 2: Job Applications

The `job_applications` table stores each job application.

| Column       | Data Type | Constraint                | Description                                               |
| ------------ | --------- | ------------------------- | --------------------------------------------------------- |
| id           | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique job application ID                                 |
| company_id   | INTEGER   | NOT NULL, FOREIGN KEY     | References `companies.id`                                 |
| job_title    | TEXT      | NOT NULL                  | Job title applied for                                     |
| source       | TEXT      | NOT NULL                  | Where the job was found, such as LinkedIn or company site |
| job_url      | TEXT      | UNIQUE                    | URL to the job post                                       |
| applied_date | DATE      | Optional                  | Date the application was submitted                        |
| salary_range | TEXT      | Optional                  | Salary range if available                                 |
| created_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP | When the record was created                               |
| updated_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP | When the record was last updated                          |

### Example

| id | company_id | job_title                  | source   | applied_date | salary_range        |
| -- | ---------- | -------------------------- | -------- | ------------ | ------------------- |
| 1  | 1          | Graduate Software Engineer | LinkedIn | 2026-07-01   | RM 4,000 - RM 6,000 |

---

## Entity 3: Statuses

The `statuses` table stores valid application status categories.

| Column          | Data Type | Constraint                | Description        |
| --------------- | --------- | ------------------------- | ------------------ |
| id              | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique status ID   |
| status_category | TEXT      | NOT NULL, UNIQUE          | Name of the status |

### Status Categories

Possible statuses:

* Saved
* Applied
* Online Assessment
* Interview
* Offer
* Rejected
* Ghosted
* Withdrawn

### Example

| id | status_category |
| -- | --------------- |
| 1  | Saved           |
| 2  | Applied         |
| 3  | Interview       |

---

## Entity 4: Job Status History

The `job_status` table stores the status history of each application.

This is useful because one job application can move through different stages over time.

| Column      | Data Type | Constraint                | Description                       |
| ----------- | --------- | ------------------------- | --------------------------------- |
| id          | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique job status history ID      |
| job_id      | INTEGER   | NOT NULL, FOREIGN KEY     | References `job_applications.id`  |
| status_id   | INTEGER   | NOT NULL, FOREIGN KEY     | References `statuses.id`          |
| status_date | DATE      | NOT NULL                  | Date when the status was recorded |

### Example

| id | job_id | status_id | status_date |
| -- | ------ | --------- | ----------- |
| 1  | 1      | 1         | 2026-06-28  |
| 2  | 1      | 2         | 2026-07-01  |
| 3  | 1      | 3         | 2026-07-10  |

This means job application `1` started as Saved, then became Applied, then moved to Interview.

---

## Entity 5: Notes

The `notes` table stores notes for each job application.

One application can have many notes.

| Column       | Data Type | Constraint                | Description                      |
| ------------ | --------- | ------------------------- | -------------------------------- |
| id           | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique note ID                   |
| job_id       | INTEGER   | NOT NULL, FOREIGN KEY     | References `job_applications.id` |
| note_details | TEXT      | NOT NULL                  | Note content                     |
| note_date    | DATE      | DEFAULT CURRENT_DATE      | Date the note was added          |

### Example

| id | job_id | note_details                        | note_date  |
| -- | ------ | ----------------------------------- | ---------- |
| 1  | 1      | Follow up if no reply after 2 weeks | 2026-07-02 |

---

## Entity 6: Skills

The `skills` table stores all possible skills found in job descriptions.

| Column     | Data Type | Constraint                | Description       |
| ---------- | --------- | ------------------------- | ----------------- |
| id         | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique skill ID   |
| skill_name | TEXT      | NOT NULL, UNIQUE          | Name of the skill |

### Example

| id | skill_name |
| -- | ---------- |
| 1  | Python     |
| 2  | SQL        |
| 3  | FastAPI    |
| 4  | React      |

---

## Entity 7: Job Skills

The `job_skills` table connects job applications to skills.

This table is needed because one job can require many skills, and one skill can appear in many jobs.

| Column   | Data Type | Constraint                | Description                      |
| -------- | --------- | ------------------------- | -------------------------------- |
| id       | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique job skill ID              |
| job_id   | INTEGER   | NOT NULL, FOREIGN KEY     | References `job_applications.id` |
| skill_id | INTEGER   | NOT NULL, FOREIGN KEY     | References `skills.id`           |

### Example

| id | job_id | skill_id |
| -- | ------ | -------- |
| 1  | 1      | 1        |
| 2  | 1      | 2        |
| 3  | 1      | 3        |

This means job application `1` requires Python, SQL, and FastAPI.

---

# Relationships

## Companies to Job Applications

Relationship:

```txt
One company can have many job applications.
One job application belongs to one company.
```

Type:

```txt
One-to-Many
```

Implementation:

```txt
job_applications.company_id references companies.id
```

Example:

```txt
Grab → Graduate Software Engineer
Grab → Backend Developer
Grab → Data Analyst
```

---

## Job Applications to Statuses

Relationship:

```txt
One job application can have many status history records.
One status category can be used by many job applications.
```

Type:

```txt
Many-to-Many through job_status
```

Implementation:

```txt
job_status.job_id references job_applications.id
job_status.status_id references statuses.id
```

Reason:

A job application can move from Saved → Applied → Interview → Offer or Rejected. The `job_status` table lets the app track the full timeline instead of only storing the latest status.

---

## Job Applications to Notes

Relationship:

```txt
One job application can have many notes.
One note belongs to one job application.
```

Type:

```txt
One-to-Many
```

Implementation:

```txt
notes.job_id references job_applications.id
```

Reason:

A user may want to record reminders, interview details, recruiter messages, or follow-up notes for each job application.

---

## Job Applications to Skills

Relationship:

```txt
One job application can require many skills.
One skill can appear in many job applications.
```

Type:

```txt
Many-to-Many through job_skills
```

Implementation:

```txt
job_skills.job_id references job_applications.id
job_skills.skill_id references skills.id
```

Reason:

Skills should not be stored as comma-separated text inside the job application row. Storing them in separate tables makes the data cleaner and easier to analyze later.

---

# Text Relationship Diagram

```txt
companies
    1 ────< job_applications
                1 ────< notes
                1 ────< job_status >──── 1 statuses
                1 ────< job_skills >──── 1 skills
```

Explanation:

```txt
companies → job_applications:
One company has many job applications.

job_applications → notes:
One job application has many notes.

job_applications → job_status → statuses:
One job application can have many status changes.

job_applications → job_skills → skills:
One job application can require many skills.
```

---

# Constraints

## companies

* `id` must be unique.
* `company_name` is required and should be unique.
* `location` is required.

## job_applications

* `id` must be unique.
* `company_id` is required.
* `job_title` is required.
* `source` is required.
* `job_url` should be unique if provided.
* `created_at` should default to the current timestamp.
* `updated_at` should default to the current timestamp.

## statuses

* `id` must be unique.
* `status_category` is required and unique.

## job_status

* `job_id` is required.
* `status_id` is required.
* `status_date` is required.

## notes

* `job_id` is required.
* `note_details` is required.
* `note_date` should default to the current date.

## skills

* `skill_name` is required and unique.

## job_skills

* `job_id` is required.
* `skill_id` is required.
* The same skill should not be duplicated for the same job application.

---

# Design Decisions

## Why is `companies` a separate table?

Companies are separated from job applications because one company can have many job posts. If company information is stored directly inside every job application row, the same company name and location will be repeated many times.

Separating companies reduces duplication and makes the database easier to update.

---

## Why is `job_status` separate from `job_applications`?

A job application does not only have one status forever. It changes over time.

Example:

```txt
Saved → Applied → Online Assessment → Interview → Rejected
```

If only the latest status is stored in the job application table, the history is lost.

The `job_status` table allows the app to track the full application timeline.

---

## Why are `skills` stored separately?

A job can require many skills, and the same skill can appear in many different job applications.

For example:

```txt
Python can appear in 20 different job applications.
One backend role can require Python, SQL, FastAPI, and Docker.
```

Because this is a many-to-many relationship, the database needs:

```txt
skills
job_skills
```

This makes it easier to count the most common skills later.

---

## Why are notes separated from job applications?

One job application can have many notes.

Example notes:

```txt
Need to follow up in 2 weeks.
Recruiter said interview will be next Monday.
Prepare SQL questions before technical interview.
```

If notes were stored directly in the job application table, it would only allow one note or force messy text. A separate notes table is cleaner.

---

# Final Table Summary

```txt
companies
- id
- company_name
- location

job_applications
- id
- company_id
- job_title
- source
- job_url
- applied_date
- salary_range
- created_at
- updated_at

statuses
- id
- status_category

job_status
- id
- job_id
- status_id
- status_date

notes
- id
- job_id
- note_details
- note_date

skills
- id
- skill_name

job_skills
- id
- job_id
- skill_id
```










