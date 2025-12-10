#!/usr/bin/env python3
"""
Test script for frontend files
"""

import os
import sys
from pathlib import Path
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestFrontendJobMatching(unittest.TestCase):
    def setUp(self):
        # Initialize the WebDriver (make sure you have ChromeDriver installed)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the browser
        self.driver.quit()

    def test_job_page_loads(self):
        """Test that the jobs page loads correctly"""
        self.driver.get("http://localhost:3000/jobs.html")
        
        # Check that the page title is correct
        self.assertIn("Job Opportunities - Scopira", self.driver.title)
        
        # Check that job results section is present
        job_results = self.wait.until(
            EC.presence_of_element_located((By.ID, "job-results"))
        )
        self.assertIsNotNone(job_results)

    def test_job_search_functionality(self):
        """Test that job search functionality works"""
        self.driver.get("http://localhost:3000/jobs.html")
        
        # Find search input fields
        search_input = self.driver.find_element(By.ID, "job-search")
        location_input = self.driver.find_element(By.ID, "job-location")
        search_button = self.driver.find_element(By.ID, "job-search-btn")
        
        # Enter search terms
        search_input.send_keys("data scientist")
        location_input.send_keys("san francisco")
        
        # Click search button
        search_button.click()
        
        # Wait for results to load
        time.sleep(2)
        
        # Check that job results are displayed
        job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card")
        # We expect at least one job card to be present
        self.assertGreater(len(job_cards), 0)

    def test_job_match_scores_displayed(self):
        """Test that job match scores are displayed"""
        self.driver.get("http://localhost:3000/jobs.html")
        
        # Wait for job results to load
        self.wait.until(
            EC.presence_of_element_located((By.ID, "job-results"))
        )
        
        # Check that match scores are displayed
        match_scores = self.driver.find_elements(By.CLASS_NAME, "match-score")
        self.assertGreater(len(match_scores), 0)
        
        # Check that each match score contains a percentage
        for score in match_scores:
            self.assertIn("%", score.text)

def check_required_files():
    """Check if all required frontend files exist"""
    print("Checking required frontend files...")
    
    required_files = [
        "index.html",
        "dashboard.html",
        "jobs.html",
        "portfolio.html",
        "profile.html",
        "css/style.css",
        "js/main.js"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join("frontend", file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
            print(f"[MISSING] Missing file: {file_path}")
        else:
            print(f"[FOUND] Found file: {file_path}")
    
    if missing_files:
        print(f"\nMissing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print(f"\n[SUCCESS] All {len(required_files)} required files found!")
    return True

def check_html_structure(file_path):
    """Check basic HTML structure of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for basic HTML structure
        if "<!DOCTYPE html>" not in content:
            print(f"  [WARNING] Missing DOCTYPE in {file_path}")
        
        if "<html" not in content:
            print(f"  [ERROR] Missing <html> tag in {file_path}")
            return False
        
        if "<head>" not in content:
            print(f"  [ERROR] Missing <head> tag in {file_path}")
            return False
        
        if "<body>" not in content:
            print(f"  [ERROR] Missing <body> tag in {file_path}")
            return False
        
        print(f"  [SUCCESS] Basic HTML structure OK in {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading {file_path}: {e}")
        return False

def test_html_files():
    """Test HTML files for basic structure"""
    print("\nTesting HTML files structure...")
    
    html_files = [
        "index.html",
        "dashboard.html",
        "jobs.html",
        "portfolio.html",
        "profile.html"
    ]
    
    all_passed = True
    
    for file_name in html_files:
        file_path = os.path.join("frontend", file_name)
        if os.path.exists(file_path):
            if not check_html_structure(file_path):
                all_passed = False
        else:
            print(f"  ❌ File not found: {file_path}")
            all_passed = False
    
    return all_passed

def check_css_references():
    """Check if HTML files reference CSS files correctly"""
    print("\nChecking CSS references in HTML files...")
    
    html_files = [
        "index.html",
        "dashboard.html",
        "jobs.html",
        "portfolio.html",
        "profile.html"
    ]
    
    all_passed = True
    
    for file_name in html_files:
        file_path = os.path.join("frontend", file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for CSS reference
                if 'href="css/style.css"' in content or "href='css/style.css'" in content:
                    print(f"  ✅ CSS reference found in {file_name}")
                else:
                    print(f"  ⚠️  CSS reference not found in {file_name}")
                    # This is not necessarily a failure, as some pages might have additional CSS
                    
            except Exception as e:
                print(f"  ❌ Error reading {file_name}: {e}")
                all_passed = False
    
    return all_passed

def check_js_references():
    """Check if HTML files reference JS files correctly"""
    print("\nChecking JavaScript references in HTML files...")
    
    html_files = [
        "index.html",
        "dashboard.html",
        "jobs.html",
        "portfolio.html",
        "profile.html"
    ]
    
    all_passed = True
    
    for file_name in html_files:
        file_path = os.path.join("frontend", file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for JS reference
                if 'src="js/main.js"' in content or "src='js/main.js'" in content:
                    print(f"  ✅ JS reference found in {file_name}")
                else:
                    print(f"  ⚠️  JS reference not found in {file_name}")
                    # This is not necessarily a failure, as some pages might not need JS
                    
            except Exception as e:
                print(f"  ❌ Error reading {file_name}: {e}")
                all_passed = False
    
    return all_passed

def main():
    """Run all frontend tests"""
    print("Running Frontend Tests\n")
    
    # Check required files
    if not check_required_files():
        return False
    
    # Test HTML structure
    if not test_html_files():
        return False
    
    # Check CSS references
    check_css_references()
    
    # Check JS references
    check_js_references()
    
    print("\n[SUCCESS] Frontend tests completed!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)