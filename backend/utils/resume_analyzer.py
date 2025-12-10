import re

class ResumeAnalyzer:
    def __init__(self):
        self.action_verbs = [
            'led', 'managed', 'developed', 'created', 'implemented', 'designed', 'analyzed',
            'improved', 'increased', 'reduced', 'saved', 'launched', 'initiated', 'coordinated',
            'collaborated', 'mentored', 'supervised', 'achieved', 'generated', 'delivered'
        ]
        
        self.weak_words = [
            'responsible for', 'duties included', 'worked on', 'helped', 'assisted', 'tried',
            'attempted', 'various', 'etc'
        ]

    def analyze(self, resume_data):
        """
        Analyze resume data and return a score and feedback.
        resume_data: dict containing 'summary', 'experience', 'education', 'skills'
        """
        score = 0
        max_score = 100
        feedback = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        # 1. Contact Info Check (Basic)
        # Assuming these are passed or we check if they exist in the data
        # For this implementation, we'll focus on content quality
        
        # 2. Summary Analysis
        summary = resume_data.get('summary', '')
        if summary:
            word_count = len(summary.split())
            if 30 <= word_count <= 100:
                score += 15
                feedback['strengths'].append("Professional summary is concise and well-length.")
            elif word_count < 30:
                score += 5
                feedback['weaknesses'].append("Professional summary is too short.")
                feedback['suggestions'].append("Expand your summary to 3-5 sentences highlighting your key achievements and career goals.")
            else:
                score += 10
                feedback['weaknesses'].append("Professional summary is a bit too long.")
                feedback['suggestions'].append("Try to condense your summary to be more punchy and readable.")
        else:
            feedback['weaknesses'].append("Missing professional summary.")
            feedback['suggestions'].append("Add a professional summary to introduce yourself to recruiters.")

        # 3. Experience Analysis
        experience = resume_data.get('experience', [])
        if experience:
            score += 20 # Base points for having experience
            
            # Check for action verbs
            action_verb_count = 0
            weak_word_count = 0
            bullet_points_count = 0
            
            for job in experience:
                details = job.get('details', [])
                # Handle if details is a string (from some legacy data) or list
                if isinstance(details, str):
                    details = [details]
                
                bullet_points_count += len(details)
                
                for point in details:
                    point_lower = point.lower()
                    if any(verb in point_lower for verb in self.action_verbs):
                        action_verb_count += 1
                    if any(word in point_lower for word in self.weak_words):
                        weak_word_count += 1
            
            # Score based on action verbs
            if bullet_points_count > 0:
                verb_ratio = action_verb_count / bullet_points_count
                if verb_ratio >= 0.5:
                    score += 20
                    feedback['strengths'].append("Great use of strong action verbs in your experience.")
                elif verb_ratio >= 0.2:
                    score += 10
                    feedback['weaknesses'].append("Could use more strong action verbs.")
                    feedback['suggestions'].append(f"Try starting bullet points with words like: {', '.join(self.action_verbs[:5])}.")
                else:
                    score += 5
                    feedback['weaknesses'].append("Experience descriptions lack impact.")
                    feedback['suggestions'].append("Rewrite bullet points to focus on achievements rather than duties. Start with action verbs.")
                
                if weak_word_count > 0:
                    feedback['suggestions'].append(f"Avoid passive phrases like 'responsible for'. Use active voice.")
            
            # Check for quantification (numbers)
            has_numbers = False
            for job in experience:
                details = job.get('details', [])
                if isinstance(details, str): details = [details]
                for point in details:
                    if re.search(r'\d+%|\$\d+|\d+ years|\d+ team members', point):
                        has_numbers = True
                        break
            
            if has_numbers:
                score += 15
                feedback['strengths'].append("Good use of metrics/numbers to quantify achievements.")
            else:
                feedback['weaknesses'].append("Lack of quantified achievements.")
                feedback['suggestions'].append("Add numbers (%, $, count) to demonstrate the impact of your work (e.g., 'Increased sales by 20%').")

        else:
            feedback['weaknesses'].append("No work experience listed.")
            feedback['suggestions'].append("Add your work history, internships, or relevant volunteer work.")

        # 4. Skills Analysis
        skills = resume_data.get('skills', [])
        # Handle if skills is a string (comma separated) or list
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',') if s.strip()]
        
        if skills:
            if len(skills) >= 5:
                score += 15
                feedback['strengths'].append("Good list of skills provided.")
            elif len(skills) > 0:
                score += 5
                feedback['weaknesses'].append("Skill list is a bit sparse.")
                feedback['suggestions'].append("Add more relevant technical and soft skills.")
        else:
            feedback['weaknesses'].append("No skills listed.")
            feedback['suggestions'].append("Add a skills section to highlight your technical and soft abilities.")

        # 5. Education Analysis
        education = resume_data.get('education', [])
        if education:
            score += 15
        else:
            feedback['weaknesses'].append("No education listed.")
            feedback['suggestions'].append("Add your educational background.")

        # Cap score at 100
        score = min(score, 100)
        
        return {
            'score': score,
            'feedback': feedback
        }
