class ResumeGenerator:
    def __init__(self):
        pass
    
    def generate_ats_friendly_resume(self, user_data, job_data):
        """
        Generate an ATS-friendly resume tailored to a specific job
        
        Args:
            user_data (dict): User's information and skills
            job_data (dict): Job description and requirements
            
        Returns:
            str: Generated resume content
        """
        # Extract key information
        user_name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
        user_email = user_data.get('email', '')
        user_phone = user_data.get('phone', '')
        user_skills = user_data.get('skills', [])
        user_experience = user_data.get('experience', [])
        
        job_title = job_data.get('title', '')
        job_company = job_data.get('company', '')
        job_requirements = job_data.get('requirements', [])
        
        # Create resume header
        resume_lines = []
        resume_lines.append(f"{user_name}")
        if user_email:
            resume_lines.append(f"{user_email}")
        if user_phone:
            resume_lines.append(f"{user_phone}")
        resume_lines.append("")  # Empty line
        
        # Professional Summary (tailored to job)
        summary = self.generate_summary(user_data, job_data)
        resume_lines.append("PROFESSIONAL SUMMARY")
        resume_lines.append(summary)
        resume_lines.append("")  # Empty line
        
        # Skills section (ATS-optimized)
        if user_skills:
            resume_lines.append("SKILLS")
            # Format skills as a comma-separated list for ATS
            skills_str = ", ".join(user_skills)
            resume_lines.append(skills_str)
            resume_lines.append("")  # Empty line
        
        # Experience section
        if user_experience:
            resume_lines.append("PROFESSIONAL EXPERIENCE")
            for exp in user_experience:
                resume_lines.append(exp)
                resume_lines.append("")  # Empty line
        
        # Education section
        education = user_data.get('education', [])
        if education:
            resume_lines.append("EDUCATION")
            for edu in education:
                resume_lines.append(edu)
                resume_lines.append("")  # Empty line
        
        return "\n".join(resume_lines)
    
    def generate_summary(self, user_data, job_data):
        """
        Generate a professional summary tailored to the job
        
        Args:
            user_data (dict): User's information
            job_data (dict): Job information
            
        Returns:
            str: Professional summary
        """
        user_skills = user_data.get('skills', [])
        job_title = job_data.get('title', 'position')
        
        # Count matching skills
        job_requirements = job_data.get('requirements', [])
        matching_skills = [skill for skill in user_skills if skill.lower() in 
                          [req.get('name', '').lower() for req in job_requirements]]
        
        if matching_skills:
            skills_text = ", ".join(matching_skills[:3])  # Limit to first 3 skills
            summary = f"Results-driven professional with expertise in {skills_text}, seeking to leverage skills and experience in the {job_title} role."
        else:
            summary = f"Dedicated professional seeking opportunities in the {job_title} field."
        
        return summary

# Example usage
if __name__ == "__main__":
    generator = ResumeGenerator()
    
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1 (555) 123-4567',
        'skills': ['Python', 'Machine Learning', 'Data Analysis', 'SQL'],
        'experience': [
            'Senior Data Analyst, Tech Corp (2020-Present)\n- Led data analysis initiatives\n- Developed machine learning models',
            'Data Analyst, Startup Inc (2018-2020)\n- Performed statistical analysis\n- Created data visualizations'
        ],
        'education': [
            'M.S. in Data Science, University (2018)',
            'B.S. in Computer Science, College (2016)'
        ]
    }
    
    job_data = {
        'title': 'Senior Data Scientist',
        'company': 'Innovative AI Company',
        'requirements': [
            {'name': 'Python'},
            {'name': 'Machine Learning'},
            {'name': 'Deep Learning'}
        ]
    }
    
    resume = generator.generate_ats_friendly_resume(user_data, job_data)
    print(resume)