# Backend API

The backend for Scopira is built with Flask, providing RESTful APIs for the frontend to interact with.

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the database:
   - Create a PostgreSQL database
   - Run the schema scripts in `../database/schemas/`

3. Configure environment variables:
   ```bash
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=postgresql://user:password@localhost/scopira
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login existing user

### Resumes
- `POST /api/resumes/upload` - Upload a resume
- `GET /api/resumes/<int:user_id>` - Get user's resumes

### Jobs
- `GET /api/jobs` - Get all jobs (with optional filtering)
- `GET /api/jobs/<int:job_id>` - Get specific job
- `GET /api/jobs/matches/<int:user_id>` - Get user's job matches
- `GET /api/jobs/recommendations/<int:user_id>` - Get job recommendations for user

### Portfolio
- `GET /api/portfolio/<int:user_id>` - Get user's portfolio
- `PUT /api/portfolio/<int:user_id>` - Update user's portfolio

## Database Models

### User
Represents a registered user with authentication information.

### Resume
Stores information about uploaded resumes and parsed data.

### Job
Contains job listings with descriptions and requirements.

### UserJobMatch
Stores match scores between users and jobs.

## Project Structure

```
backend/
├── app.py              # Main application entry point
├── requirements.txt    # Python dependencies
├── models/             # Database models
│   ├── __init__.py
│   ├── db.py           # Database initialization
│   ├── user.py         # User model
│   ├── resume.py       # Resume model
│   ├── job.py          # Job model
│   └── user_job_match.py # User-job match model
├── routes/             # API routes
│   ├── __init__.py
│   ├── auth_routes.py  # Authentication routes
│   ├── resume_routes.py # Resume routes
│   ├── job_routes.py   # Job routes
│   └── portfolio_routes.py # Portfolio routes
└── utils/              # Utility functions
```