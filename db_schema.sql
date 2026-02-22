CREATE DATABASE student_data;
USE student_data;

CREATE TABLE students (
    student_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(50),
    email VARCHAR(255),
    phone VARCHAR(255),
    enrollment_year INT,
    course_batch VARCHAR(50),
    city VARCHAR(255),
    graduation_year INT
);
CREATE TABLE programming (
    programming_id VARCHAR(255) PRIMARY KEY,
    student_id VARCHAR(255),
    language VARCHAR(50),
    problems_solved INT,
    assessments_completed INT,
    mini_projects INT,
    certifications_earned INT,
    latest_project_score DECIMAL(5, 2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE soft_skills (
    soft_skill_id VARCHAR(255) PRIMARY KEY,
    student_id VARCHAR(255),
    communication INT,
    teamwork INT,
    presentation INT,
    leadership INT,
    critical_thinking INT,
    interpersonal_skills INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE placements (
    placement_id VARCHAR(255) PRIMARY KEY,
    student_id VARCHAR(255),
    mock_interview_score INT,
    internships_completed INT,
    placement_status VARCHAR(50),
    company_name VARCHAR(255),
    placement_package DECIMAL(10, 2),
    interview_rounds_cleared INT,
    placement_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);