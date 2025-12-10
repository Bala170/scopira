# Machine Learning Components

This directory contains all the machine learning components for the Scopira platform.

## Components

### Resume Parser (`resume_parser.py`)
- Extracts information from PDF and DOCX resumes
- Uses spaCy for Named Entity Recognition (NER)
- Identifies skills, experience, and contact information

### Job Matcher (`job_matcher.py`)
- Calculates similarity between user profiles and job descriptions
- Uses TF-IDF and cosine similarity
- Matches user skills with job requirements

### Skill Gap Analyzer (`skill_gap_analyzer.py`)
- Compares user skills with job requirements
- Identifies missing skills
- Generates learning recommendations

### Resume Generator (`resume_generator.py`)
- Creates ATS-friendly resumes
- Tailors resumes to specific job roles
- Optimizes keyword usage

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Download spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Each component can be used independently or as part of the full pipeline:

```python
# Example usage
from scripts.resume_parser import ResumeParser
from scripts.job_matcher import JobMatcher
from scripts.skill_gap_analyzer import SkillGapAnalyzer
from scripts.resume_generator import ResumeGenerator

# Parse a resume
parser = ResumeParser()
parsed_data = parser.parse_pdf("path/to/resume.pdf")

# Match user to jobs
matcher = JobMatcher()
similarities = matcher.calculate_similarity(user_profile, job_descriptions)

# Analyze skill gaps
analyzer = SkillGapAnalyzer()
gaps = analyzer.analyze_gaps(user_skills, job_requirements)

# Generate optimized resume
generator = ResumeGenerator()
resume = generator.generate_ats_friendly_resume(user_data, job_data)
```