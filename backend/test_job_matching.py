import unittest
import json
import sys
import os

# Add the backend directory to the path so we can import models directly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from models.db import db
from models.user import User
from models.job import Job
from models.resume import Resume
from models.user_job_match import UserJobMatch
from models.portfolio import Portfolio

class TestJobMatching(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create all tables
        with app.app_context():
            # Configure test database
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
            # Create all tables
            db.create_all()
            
            # Create test user
            user = User(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            user.set_password('password123')
            db.session.add(user)
            
            # Create test job
            job = Job(
                title='Data Scientist',
                company='Tech Corp',
                description='Looking for experienced data scientist',
                requirements=json.dumps({'skills': ['python', 'machine learning', 'sql']}),
                location='San Francisco, CA',
                salary_range='$100k - $150k'
            )
            db.session.add(job)
            
            # Create test resume with skills
            resume = Resume(
                user_id=1,
                file_path='/path/to/resume.pdf',
                original_filename='resume.pdf',
                skills=json.dumps(['python', 'sql', 'data analysis'])
            )
            db.session.add(resume)
            
            db.session.commit()

    def tearDown(self):
        """Clean up test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_jobs(self):
        """Test getting jobs"""
        with app.app_context():
            response = self.app.get('/api/jobs/')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('jobs', data)
            self.assertGreater(len(data['jobs']), 0)

    def test_get_job_recommendations(self):
        """Test getting job recommendations for a user"""
        with app.app_context():
            response = self.app.get('/api/jobs/recommendations/1')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('recommendations', data)
            self.assertGreater(len(data['recommendations']), 0)
            
            # Check that match scores are calculated
            recommendation = data['recommendations'][0]
            self.assertIn('match_score', recommendation)
            self.assertIn('matched_skills', recommendation)
            self.assertIn('missing_skills', recommendation)

    def test_calculate_job_match(self):
        """Test calculating job match between user and job"""
        with app.app_context():
            # First, get a job to match against
            job = Job.query.first()
            
            response = self.app.post('/api/jobs/match', 
                                   data=json.dumps({
                                       'user_id': 1,
                                       'job_id': job.id
                                   }),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 201)
            
            data = json.loads(response.data)
            self.assertIn('match_score', data)
            self.assertIn('matched_skills', data)
            self.assertIn('missing_skills', data)
            
            # Check that match was saved to database
            match = UserJobMatch.query.filter_by(user_id=1, job_id=job.id).first()
            self.assertIsNotNone(match)

    def test_get_user_job_matches(self):
        """Test getting user job matches"""
        # First create a match
        with app.app_context():
            job = Job.query.first()
            match = UserJobMatch(
                user_id=1,
                job_id=job.id,
                match_score=0.8,
                matched_skills=json.dumps(['python', 'sql']),
                missing_skills=json.dumps(['machine learning'])
            )
            db.session.add(match)
            db.session.commit()
            
            response = self.app.get('/api/jobs/matches/1')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('matches', data)
            self.assertGreater(len(data['matches']), 0)
            
            match_data = data['matches'][0]
            self.assertIn('job', match_data)
            self.assertIn('match_score', match_data)

    def test_get_job_recommendations_with_portfolio(self):
        """Test getting job recommendations for a user with only portfolio"""
        with app.app_context():
            # Create a new user without resume
            user = User(
                username='portfoliouser',
                email='portfolio@example.com',
                first_name='Portfolio',
                last_name='User'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Create portfolio with skills
            portfolio = Portfolio(
                user_id=user.id,
                skills=json.dumps({
                    'technical': ['python', 'sql'],
                    'soft': ['communication']
                })
            )
            db.session.add(portfolio)
            db.session.commit()
            
            response = self.app.get(f'/api/jobs/recommendations/{user.id}')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('recommendations', data)
            self.assertGreater(len(data['recommendations']), 0)
            
            # Check that match scores are calculated based on portfolio skills
            recommendation = data['recommendations'][0]
            self.assertIn('match_score', recommendation)
            # Should match python and sql
            self.assertGreater(recommendation['match_score'], 0)

if __name__ == '__main__':
    unittest.main()