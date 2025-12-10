# Scopira - AI-Powered Career Guidance Platform

Scopira is an AI-powered career guidance platform that helps users optimize their careers through personalized job recommendations, skill gap analysis, and AI-generated resumes.

## Features

### User Authentication
- Secure signup and login
- Profile management

### Resume Upload & Parsing
- Upload resumes in PDF or DOCX format
- AI-powered parsing to extract skills and experience

### Job Matching Engine
- Personalized job recommendations
- Hybrid similarity model (TF-IDF + Sentence-BERT)
- Match scoring and ranking

### Skill Gap Analyzer
- Compare user profile vs. job requirements
- Identify missing skills
- Recommend learning resources

### AI Resume Maker
- Generate ATS-friendly resumes
- Role-specific templates
- Customizable sections

### Portfolio Creator
- Web-based personal portfolio
- Skills, projects, and certifications showcase
- Interactive elements

### Explainable Dashboard
- Radar charts and bar graphs
- Skill strength visualization
- Job match explanations

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Responsive design
- Chart.js for data visualization

### Backend
- Flask (Python)
- SQLAlchemy for ORM
- RESTful API architecture

### Database
- PostgreSQL (recommended)
- SQL schema definitions

### Machine Learning
- spaCy for NLP and entity extraction
- scikit-learn for similarity matching
- Custom algorithms for skill gap analysis

## Project Structure

```
scopira/
├── frontend/           # HTML, CSS, JavaScript frontend
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   ├── assets/         # Images and other assets
│   ├── index.html      # Landing page
│   ├── dashboard.html  # User dashboard
│   ├── jobs.html       # Job listings and search
│   ├── portfolio.html  # Interactive portfolio
│   └── profile.html    # User profile management
├── backend/            # Flask backend
│   ├── controllers/    # Request handlers
│   ├── models/         # Database models
│   ├── routes/         # API routes
│   ├── utils/          # Utility functions
│   ├── app.py          # Main application
│   └── requirements.txt # Python dependencies
├── ml/                 # Machine Learning components
│   ├── models/         # Trained models
│   ├── scripts/        # ML scripts
│   └── data/           # Training data
├── database/           # Database schemas
│   ├── schemas/        # Database schema definitions
│   └── migrations/     # Database migrations
└── uploads/            # User uploaded files
```

## Getting Started

1. Clone the repository
2. Set up the backend environment:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the ML environment:
   ```bash
   cd ml
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. Set up the database:
   - Install PostgreSQL
   - Create a PostgreSQL database
   - Run the schema scripts in `database/schemas/`

5. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```

6. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

7. Open `http://localhost:8000` in a browser

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/resumes/upload` - Upload resume
- `GET /api/jobs` - Get job listings
- `GET /api/jobs/matches/{user_id}` - Get user job matches
- `GET /api/portfolio/{user_id}` - Get user portfolio

## ML Components

- `resume_parser.py` - Extract information from resumes
- `job_matcher.py` - Match users to jobs
- `skill_gap_analyzer.py` - Analyze skill gaps
- `resume_generator.py` - Generate optimized resumes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

