import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class JobMatcher:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    
    def calculate_similarity(self, user_profile, job_descriptions):
        """
        Calculate similarity between user profile and job descriptions
        
        Args:
            user_profile (str): User's resume/profile text
            job_descriptions (list): List of job description texts
            
        Returns:
            list: Similarity scores for each job
        """
        # Combine user profile with job descriptions for vectorization
        texts = [user_profile] + job_descriptions
        
        # Vectorize texts
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity between user profile and each job
        user_vector = tfidf_matrix[0]
        job_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(user_vector, job_vectors)
        
        # Return similarity scores as a list
        return similarities[0].tolist()
    
    def match_user_to_jobs(self, user_skills, job_requirements):
        """
        Match user skills to job requirements
        
        Args:
            user_skills (list): List of user's skills
            job_requirements (list): List of job requirement dictionaries
            
        Returns:
            dict: Matching results with scores and skill gaps
        """
        results = []
        
        user_skills_set = set(skill.lower() for skill in user_skills)
        
        for job in job_requirements:
            job_skills_set = set(skill.lower() for skill in job.get('skills', []))
            
            # Calculate match score
            if job_skills_set:
                matched_skills = user_skills_set.intersection(job_skills_set)
                missing_skills = job_skills_set.difference(user_skills_set)
                
                match_score = len(matched_skills) / len(job_skills_set)
                
                results.append({
                    'job_id': job.get('id'),
                    'match_score': match_score,
                    'matched_skills': list(matched_skills),
                    'missing_skills': list(missing_skills)
                })
            else:
                results.append({
                    'job_id': job.get('id'),
                    'match_score': 0,
                    'matched_skills': [],
                    'missing_skills': []
                })
        
        return results

# Example usage
if __name__ == "__main__":
    matcher = JobMatcher()
    
    # Example user profile and job descriptions
    user_profile = "Experienced Python developer with skills in machine learning and data analysis"
    job_descriptions = [
        "Looking for Python developer with machine learning experience",
        "Seeking Java developer with Spring framework experience",
        "Need data scientist with Python and statistics background"
    ]
    
    # Calculate similarities
    similarities = matcher.calculate_similarity(user_profile, job_descriptions)
    
    for i, score in enumerate(similarities):
        print(f"Job {i+1} similarity score: {score:.3f}")