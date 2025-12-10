# Scopira Platform Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Components](#components)
   - [Frontend](#frontend)
   - [Backend](#backend)
   - [Machine Learning](#machine-learning)
   - [Database](#database)
5. [API Reference](#api-reference)
6. [Development](#development)
7. [Deployment](#deployment)

## Overview

Scopira is an AI-powered career guidance platform that helps users optimize their careers through personalized job recommendations, skill gap analysis, and AI-generated resumes.

The platform consists of four main components:
- **Frontend**: User interface built with HTML, CSS, and JavaScript
- **Backend**: Flask-based REST API
- **Machine Learning**: Python scripts for resume parsing, job matching, and skill analysis
- **Database**: PostgreSQL database for storing user data, resumes, and job listings

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │ Machine Learning│
│  (HTML/CSS/JS)  │◄──►│   (Flask API)   │◄──►│   (Python ML)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │   Database      │
                        │  (PostgreSQL)   │
                        └─────────────────┘
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js and npm
- PostgreSQL
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd scopira
   ```

2. Run the setup script:
   ```bash
   python setup.py
   ```

3. Initialize the database:
   ```bash
   python database/init_db.py
   ```

## Components

### Frontend

#### Technologies
- HTML5
- CSS3
- JavaScript (ES6+)
- Chart.js for data visualization

#### Pages
- **Landing Page** (`index.html`): Platform overview and feature highlights
- **Dashboard** (`dashboard.html`): User dashboard with skill visualizations
- **Jobs** (`jobs.html`): Job search and application interface
- **Portfolio** (`portfolio.html`): Interactive portfolio showcase
- **Profile** (`profile.html`): User profile management

#### Key Features
- Responsive design for all device sizes
- Interactive data visualizations
- Form validation and user input handling
- API integration with backend services

### Backend

#### Technologies
- Flask (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (database)

#### API Endpoints
- **Authentication**: `/api/auth/*`
- **Resumes**: `/api/resumes/*`
- **Jobs**: `/api/jobs/*`
- **Portfolio**: `/api/portfolio/*`

#### Key Features
- RESTful API design
- User authentication and session management
- Database integration with SQLAlchemy
- File upload and management

### Machine Learning

#### Technologies
- spaCy (NLP and entity extraction)
- scikit-learn (machine learning algorithms)
- pandas and numpy (data processing)

#### Components
- **Resume Parser**: Extracts information from PDF/DOCX resumes
- **Job Matcher**: Matches users to jobs based on skills and experience
- **Skill Gap Analyzer**: Identifies missing skills and recommends learning resources
- **Resume Generator**: Creates ATS-friendly resumes tailored to specific jobs

#### Key Features
- Named Entity Recognition for resume parsing
- TF-IDF and cosine similarity for job matching
- Custom algorithms for skill gap analysis
- Template-based resume generation

### Database

#### Technologies
- PostgreSQL
- SQL schema definitions

#### Tables
- **Users**: User authentication and profile information
- **Resumes**: Uploaded resumes and parsed data
- **Jobs**: Job listings with descriptions and requirements
- **User-Job Matches**: Match scores between users and jobs
- **Skills**: Master list of skills
- **User Skills**: User proficiency in various skills
- **Job Skills**: Skills required for specific jobs

## API Reference

### Authentication
```
POST /api/auth/register
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string"
}

POST /api/auth/login
{
  "username": "string",
  "password": "string"
}
```

### Resumes
```
POST /api/resumes/upload
Content-Type: multipart/form-data
file: resume.pdf
user_id: 123

GET /api/resumes/{user_id}
```

### Jobs
```
GET /api/jobs
Query Parameters: location, title

GET /api/jobs/{job_id}

GET /api/jobs/matches/{user_id}

GET /api/jobs/recommendations/{user_id}
```

### Portfolio
```
GET /api/portfolio/{user_id}

PUT /api/portfolio/{user_id}
{
  "skills": [...],
  "projects": [...],
  "experience": [...]
}
```

## Development

### Directory Structure
```
scopira/
├── frontend/     # User interface
├── backend/      # Flask API
├── ml/           # Machine learning components
├── database/     # Database schemas and scripts
└── uploads/      # User uploaded files
```

### Running Development Servers
```bash
python run_dev.py
```

### Testing
- Unit tests for backend API endpoints
- Integration tests for ML components
- End-to-end tests for frontend functionality

## Deployment

### Production Setup
1. Configure environment variables
2. Set up PostgreSQL database
3. Deploy backend Flask application
4. Serve frontend static files
5. Configure reverse proxy (Nginx/Apache)
6. Set up SSL certificates

### Environment Variables
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
UPLOAD_FOLDER=/path/to/uploads
```

### Scaling Considerations
- Use a WSGI server (Gunicorn/uWSGI) for Flask
- Implement database connection pooling
- Use CDN for static assets
- Implement caching for frequently accessed data
- Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.