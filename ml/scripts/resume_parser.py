import spacy
from PyPDF2 import PdfReader
import docx
import json
import re

class ResumeParser:
    def __init__(self):
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Please install spaCy English model: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def parse_pdf(self, file_path):
        """Parse PDF resume and extract information"""
        reader = PdfReader(file_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return self.extract_info(text)
    
    def parse_docx(self, file_path):
        """Parse DOCX resume and extract information"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return self.extract_info(text)
    
    def extract_info(self, text):
        """Extract information from resume text"""
        # Process text with spaCy
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract named entities
            entities = {
                'PERSON': [],
                'ORG': [],
                'GPE': [],  # Geopolitical entity (locations)
                'EMAIL': [],
                'PHONE': []
            }
            
            for ent in doc.ents:
                if ent.label_ in entities:
                    entities[ent.label_].append(ent.text)
            
            # Extract email addresses using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            entities['EMAIL'] = emails
            
            # Extract phone numbers using regex
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, text)
            entities['PHONE'] = phones
            
            # Extract skills (simplified approach)
            skills_keywords = [
                'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'node.js',
                'machine learning', 'data analysis', 'project management', 'communication',
                'leadership', 'teamwork', 'problem solving', 'critical thinking'
            ]
            
            skills = []
            text_lower = text.lower()
            for skill in skills_keywords:
                if skill in text_lower:
                    skills.append(skill)
            
            # Extract experience sections
            experience_sections = self.extract_experience(text)
            
            return {
                'entities': entities,
                'skills': skills,
                'experience': experience_sections
            }
        else:
            # Fallback if spaCy is not available
            return {
                'text': text,
                'skills': [],
                'experience': []
            }
    
    def extract_experience(self, text):
        """Extract experience sections from resume"""
        # Simple approach to find experience sections
        experience_keywords = ['experience', 'work history', 'employment']
        sections = []
        
        lines = text.split('\n')
        in_experience_section = False
        current_section = ""
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line starts an experience section
            if any(keyword in line_lower for keyword in experience_keywords):
                if current_section:
                    sections.append(current_section)
                current_section = line + "\n"
                in_experience_section = True
            elif in_experience_section:
                # Check if we've reached the end of the experience section
                if line_lower in ['education', 'skills', 'projects', 'certifications'] or \
                   (line_lower == '' and len(current_section.split('\n')) > 10):
                    sections.append(current_section)
                    in_experience_section = False
                    current_section = ""
                else:
                    current_section += line + "\n"
        
        # Add the last section if it exists
        if current_section:
            sections.append(current_section)
        
        return sections

# Example usage
if __name__ == "__main__":
    parser = ResumeParser()
    # Example: parsed_data = parser.parse_pdf("path/to/resume.pdf")
    # print(json.dumps(parsed_data, indent=2))