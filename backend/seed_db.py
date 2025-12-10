import sys
import os
import json
from datetime import datetime

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Change to the backend directory
os.chdir(backend_dir)

# Set the PYTHONPATH environment variable
os.environ['PYTHONPATH'] = backend_dir

from app import app
from models.db import db
from models.user import User
from models.job import Job
from models.resume import Resume
from models.portfolio import Portfolio
from werkzeug.security import generate_password_hash

def seed_db():
    with app.app_context():
        print("Seeding database...")
        
        # Create a test user if not exists
        user = User.query.filter_by(email='john@example.com').first()
        if not user:
            user = User(
                username='johndoe',
                email='john@example.com',
                password_hash=generate_password_hash('password'),
                first_name='John',
                last_name='Doe',
                phone='+1 (555) 123-4567',
                location='San Francisco, CA',
                headline='Senior Data Scientist',
                summary='Passionate data scientist with 5+ years of experience in machine learning, statistical analysis, and data visualization. Specialize in Python, TensorFlow, and cloud-based data solutions.',
                profession='Data Scientist'
            )
            db.session.add(user)
            db.session.commit()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
            
        # Create portfolio for user
        portfolio = Portfolio.query.filter_by(user_id=user.id).first()
        if not portfolio:
            portfolio = Portfolio(
                user_id=user.id,
                skills=json.dumps({
                    "technical": ["Python", "Machine Learning", "TensorFlow", "SQL", "Data Visualization", "Statistical Analysis"],
                    "soft": ["Communication", "Problem Solving", "Leadership", "Team Collaboration"]
                }),
                experience=json.dumps([
                    {
                        "title": "Senior Data Scientist",
                        "company": "TechCorp Inc.",
                        "duration": "Jan 2022 - Present",
                        "description": "Lead machine learning initiatives and mentor junior data scientists. Developed recommendation systems that increased user engagement by 35%."
                    },
                    {
                        "title": "Data Scientist",
                        "company": "DataSystems Ltd",
                        "duration": "Mar 2020 - Dec 2021",
                        "description": "Built predictive models for customer behavior analysis. Reduced customer churn by 20% through targeted interventions."
                    }
                ]),
                education=json.dumps([
                    {
                        "degree": "Master of Science in Data Science",
                        "institution": "Stanford University",
                        "duration": "2016 - 2018"
                    },
                    {
                        "degree": "Bachelor of Science in Computer Science",
                        "institution": "MIT",
                        "duration": "2012 - 2016"
                    }
                ]),
                projects=json.dumps([
                    {
                        "title": "Customer Churn Prediction",
                        "description": "Developed a machine learning model to predict customer churn with 92% accuracy, saving the company $2M annually.",
                        "tags": "Python, Scikit-learn, Data Analysis"
                    }
                ]),
                certifications=json.dumps([
                    {
                        "title": "Google Professional Data Engineer",
                        "issuer": "Google Cloud",
                        "date": "Issued: Mar 2023"
                    }
                ]),
                preferences=json.dumps({
                    "roles": "Data Scientist, Machine Learning Engineer",
                    "location": "San Francisco, CA; Remote",
                    "salary": "$130,000 - $160,000",
                    "type": "full-time",
                    "environment": "remote"
                })
            )
            db.session.add(portfolio)
            db.session.commit()
            print(f"Created portfolio for user: {user.username}")
        else:
            print(f"Portfolio already exists for user: {user.username}")

        # Create some jobs
        jobs_data = [
            {
                "title": "Senior Data Scientist",
                "company": "TechCorp Inc.",
                "location": "San Francisco, CA",
                "salary_range": "$120,000 - $150,000",
                "description": "Join our team to build cutting-edge machine learning models and drive data-driven decisions.",
                "requirements": json.dumps({"skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Statistics"]})
            },
            {
                "title": "Frontend Developer",
                "company": "WebSolutions Ltd.",
                "location": "New York, NY",
                "salary_range": "$90,000 - $110,000",
                "description": "Create beautiful, responsive web applications using modern JavaScript frameworks.",
                "requirements": json.dumps({"skills": ["JavaScript", "React", "HTML/CSS", "REST APIs"]})
            },
            {
                "title": "UX Designer",
                "company": "DesignHub",
                "location": "Remote",
                "salary_range": "$85,000 - $105,000",
                "description": "Design intuitive user experiences for web and mobile applications.",
                "requirements": json.dumps({"skills": ["Figma", "User Research", "Prototyping", "UI Design"]})
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudTech",
                "location": "Austin, TX",
                "salary_range": "$110,000 - $130,000",
                "description": "Implement and maintain scalable cloud infrastructure and CI/CD pipelines.",
                "requirements": json.dumps({"skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform"]})
            },
            {
                "title": "Product Manager",
                "company": "InnovateCo",
                "location": "Seattle, WA",
                "salary_range": "$100,000 - $125,000",
                "description": "Lead product development from conception to launch, working with cross-functional teams.",
                "requirements": json.dumps({"skills": ["Product Strategy", "Agile", "Market Research", "Stakeholder Management"]})
            }
        ]
        
        for job_data in jobs_data:
            job = Job.query.filter_by(title=job_data['title'], company=job_data['company']).first()
            if not job:
                job = Job(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    salary_range=job_data['salary_range'],
                    description=job_data['description'],
                    requirements=job_data['requirements']
                )
                db.session.add(job)
                print(f"Created job: {job.title}")
            else:
                print(f"Job already exists: {job.title}")
        
        db.session.commit()
        print("Database seeding completed!")

if __name__ == '__main__':
    seed_db()
