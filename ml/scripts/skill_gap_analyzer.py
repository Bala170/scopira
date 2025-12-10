import json

class SkillGapAnalyzer:
    def __init__(self):
        pass
    
    def analyze_gaps(self, user_skills, job_requirements):
        """
        Analyze skill gaps between user and job requirements
        
        Args:
            user_skills (list): List of user's skills
            job_requirements (dict): Job requirements with skills and importance
            
        Returns:
            dict: Analysis results including gaps and recommendations
        """
        user_skills_set = set(skill.lower() for skill in user_skills)
        job_skills = job_requirements.get('skills', [])
        
        matched_skills = []
        missing_skills = []
        
        for skill in job_skills:
            skill_name = skill.get('name', '').lower()
            importance = skill.get('importance', 1)
            
            if skill_name in user_skills_set:
                matched_skills.append({
                    'name': skill_name,
                    'importance': importance
                })
            else:
                missing_skills.append({
                    'name': skill_name,
                    'importance': importance
                })
        
        # Calculate match percentage
        total_skills = len(job_skills)
        matched_count = len(matched_skills)
        match_percentage = (matched_count / total_skills * 100) if total_skills > 0 else 0
        
        # Generate recommendations
        recommendations = self.generate_recommendations(missing_skills)
        
        return {
            'match_percentage': match_percentage,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, missing_skills):
        """
        Generate learning recommendations for missing skills
        
        Args:
            missing_skills (list): List of missing skills
            
        Returns:
            list: Learning recommendations
        """
        # This is a simplified recommendation system
        # In a real implementation, this would integrate with learning platforms like Coursera
        recommendations = []
        
        # Common learning resources for popular skills
        learning_resources = {
            'python': {
                'type': 'Online Course',
                'platform': 'Coursera',
                'title': 'Python for Everybody',
                'url': 'https://www.coursera.org/specializations/python'
            },
            'machine learning': {
                'type': 'Online Course',
                'platform': 'Coursera',
                'title': 'Machine Learning',
                'url': 'https://www.coursera.org/learn/machine-learning'
            },
            'data analysis': {
                'type': 'Online Course',
                'platform': 'Coursera',
                'title': 'Data Analysis and Visualization',
                'url': 'https://www.coursera.org/specializations/data-analysis'
            },
            'sql': {
                'type': 'Online Course',
                'platform': 'Coursera',
                'title': 'SQL for Data Science',
                'url': 'https://www.coursera.org/learn/sql-for-data-science'
            }
        }
        
        for skill in missing_skills:
            skill_name = skill['name']
            if skill_name in learning_resources:
                recommendation = learning_resources[skill_name].copy()
                recommendation['skill'] = skill_name
                recommendation['importance'] = skill['importance']
                recommendations.append(recommendation)
        
        return recommendations

# Example usage
if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    
    user_skills = ['python', 'sql', 'data analysis']
    job_requirements = {
        'skills': [
            {'name': 'python', 'importance': 5},
            {'name': 'machine learning', 'importance': 4},
            {'name': 'sql', 'importance': 3},
            {'name': 'deep learning', 'importance': 2}
        ]
    }
    
    gaps = analyzer.analyze_gaps(user_skills, job_requirements)
    print(json.dumps(gaps, indent=2))