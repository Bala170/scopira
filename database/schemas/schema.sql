-- Database schema for Scopira platform

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    file_path VARCHAR(200) NOT NULL,
    original_filename VARCHAR(100) NOT NULL,
    parsed_data TEXT, -- JSON string of parsed resume data
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    full_name VARCHAR(100),
    email VARCHAR(120),
    phone VARCHAR(20),
    summary TEXT
);

-- Jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT, -- JSON string of required skills
    location VARCHAR(100),
    salary_range VARCHAR(50),
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

-- User-Job Matches table
CREATE TABLE user_job_matches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    job_id INTEGER REFERENCES jobs(id) NOT NULL,
    match_score FLOAT, -- Between 0 and 1
    matched_skills TEXT, -- JSON string of matched skills
    missing_skills TEXT, -- JSON string of missing skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);

-- User Skills table
CREATE TABLE user_skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    skill_id INTEGER REFERENCES skills(id) NOT NULL,
    proficiency_level INTEGER, -- 1-5 scale
    years_of_experience FLOAT
);

-- Job Skills table
CREATE TABLE job_skills (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) NOT NULL,
    skill_id INTEGER REFERENCES skills(id) NOT NULL,
    importance_level INTEGER -- 1-5 scale
);