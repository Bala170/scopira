// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 70,
                behavior: 'smooth'
            });
        }
    });
});

// Form validation for resume upload
function validateResumeUpload() {
    const fileInput = document.getElementById('resume-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file to upload');
        return false;
    }
    
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(file.type)) {
        alert('Please upload a PDF or DOCX file');
        return false;
    }
    
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        alert('File size exceeds 5MB limit');
        return false;
    }
    
    return true;
}

// Job search functionality
function searchJobs() {
    const searchTerm = document.getElementById('job-search').value.toLowerCase();
    const location = document.getElementById('job-location').value.toLowerCase();
    
    // Build query parameters
    const params = new URLSearchParams();
    if (searchTerm) params.append('title', searchTerm);
    if (location) params.append('location', location);
    
    // Display loading message
    const resultsContainer = document.getElementById('job-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '<p>Searching for jobs...</p>';
    }
    
    // Make API call to search jobs
    fetch(`http://localhost:5000/api/jobs?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (resultsContainer) {
                displayJobs(data.jobs);
            }
        })
        .catch(error => {
            console.error('Error searching jobs:', error);
            if (resultsContainer) {
                resultsContainer.innerHTML = '<p>Error loading jobs. Please try again later.</p>';
            }
        });
}

// Display jobs in the job results container
function displayJobs(jobs) {
    const resultsContainer = document.getElementById('job-results');
    
    if (!resultsContainer) return;
    
    if (!jobs || jobs.length === 0) {
        resultsContainer.innerHTML = '<p>No jobs found matching your criteria.</p>';
        return;
    }
    
    resultsContainer.innerHTML = jobs.map(job => `
        <div class="job-card">
            <div class="job-header">
                <h3>${job.title || 'Job Title'}</h3>
                <span class="match-score">${Math.floor(Math.random() * 40 + 60)}% Match</span>
            </div>
            <p class="company"><i class="fas fa-building"></i> ${job.company || 'Company Name'}</p>
            <p class="location"><i class="fas fa-map-marker-alt"></i> ${job.location || 'Location'}</p>
            <p class="salary"><i class="fas fa-dollar-sign"></i> ${job.salary_range || 'Salary Range'}</p>
            <p class="description">${job.description || 'Job description not available.'}</p>
            <div class="job-tags">
                <!-- Tags would be populated based on job requirements -->
                <span class="tag">Python</span>
                <span class="tag">Machine Learning</span>
                <span class="tag">SQL</span>
            </div>
            <div class="job-actions">
                <button class="btn primary-btn">Apply Now</button>
                <button class="btn secondary-btn">Save Job</button>
            </div>
        </div>
    `).join('');
}

// Initialize dashboard charts (using Chart.js)
function initDashboard() {
    // Skill radar chart
    const radarCtx = document.getElementById('skills-radar');
    if (radarCtx) {
        const radarChart = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Python', 'JavaScript', 'Machine Learning', 'Data Analysis', 'Communication', 'Leadership'],
                datasets: [{
                    label: 'Your Skills',
                    data: [85, 70, 90, 80, 75, 65],
                    backgroundColor: 'rgba(67, 97, 238, 0.2)',
                    borderColor: 'rgba(67, 97, 238, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(67, 97, 238, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(67, 97, 238, 1)'
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: {
                            display: true,
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        pointLabels: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 14
                            },
                            color: '#333'
                        }
                    }
                }
            }
        });
    }
    
    // Job match bar chart
    const barCtx = document.getElementById('job-match-chart');
    if (barCtx) {
        const barChart = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Data Scientist', 'ML Engineer', 'Software Dev', 'Data Analyst', 'AI Researcher'],
                datasets: [{
                    label: 'Match Percentage',
                    data: [92, 85, 78, 88, 75],
                    backgroundColor: [
                        'rgba(67, 97, 238, 0.7)',
                        'rgba(67, 97, 238, 0.6)',
                        'rgba(67, 97, 238, 0.5)',
                        'rgba(67, 97, 238, 0.4)',
                        'rgba(67, 97, 238, 0.3)'
                    ],
                    borderColor: [
                        'rgba(67, 97, 238, 1)',
                        'rgba(67, 97, 238, 1)',
                        'rgba(67, 97, 238, 1)',
                        'rgba(67, 97, 238, 1)',
                        'rgba(67, 97, 238, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 5,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            color: '#666',
                            font: {
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#666',
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(67, 97, 238, 0.9)',
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        padding: 12
                    }
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard if on dashboard page
    if (document.getElementById('dashboard')) {
        initDashboard();
    }
    
    // Add event listeners for forms
    const uploadForm = document.getElementById('resume-upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateResumeUpload()) {
                // In a real implementation, this would upload the file
                alert('Resume uploaded successfully!');
            }
        });
    }
    
    // Add event listener for job search
    const searchButton = document.getElementById('job-search-btn');
    if (searchButton) {
        searchButton.addEventListener('click', searchJobs);
    }
    
    // Load jobs on the jobs page
    if (document.getElementById('jobs')) {
        loadJobRecommendations();
    }
    
    // Profile image upload simulation
    const profileImage = document.querySelector('.profile-image img');
    if (profileImage) {
        profileImage.addEventListener('click', function() {
            // In a real implementation, this would open a file dialog
            console.log('Profile image clicked - would open file dialog');
        });
    }
    
    // Resume upload functionality
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('resume-file');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const fileName = this.files[0].name;
                const fileSize = (this.files[0].size / (1024 * 1024)).toFixed(2); // in MB
                
                // Validate file type
                const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
                if (!allowedTypes.includes(this.files[0].type)) {
                    alert('Please upload a PDF or DOCX file');
                    return;
                }
                
                // Validate file size (5MB limit)
                if (this.files[0].size > 5 * 1024 * 1024) {
                    alert('File size exceeds 5MB limit');
                    return;
                }
                
                // In a real implementation, this would upload the file
                alert(`File selected: ${fileName} (${fileSize} MB)\nIn a real implementation, this would upload the file.`);
            }
        });
    }
    
    // Form submission handlers
    const profileForms = document.querySelectorAll('.profile-form');
    profileForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const formObject = {};
            formData.forEach((value, key) => {
                formObject[key] = value;
            });
            
            // In a real implementation, this would send data to the server
            console.log('Form submitted:', formObject);
            alert('Changes saved successfully!');
        });
    });
    
    // Delete buttons functionality
    document.querySelectorAll('.resume-actions .btn, .experience-actions .btn, .education-actions .btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.querySelector('.fa-trash')) {
                if (confirm('Are you sure you want to delete this item?')) {
                    this.closest('.resume-item, .experience-item, .education-item').remove();
                }
            }
        });
    });
    
    // Account deletion
    const deleteAccountBtn = document.querySelector('#settings .settings-section .btn');
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
                // In a real implementation, this would delete the account
                alert('Account deletion functionality would be implemented here.');
            }
        });
    }
    
    // Robust Logout: delegate click to handle dynamic menu/content
    document.addEventListener('click', function(e) {
        const logoutEl = e.target.closest('#logout-btn');
        if (logoutEl) {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                try {
                    // Clear any session state
                    localStorage.removeItem('user');
                } catch (_) {}
                // Lightweight feedback
                alert('You have been logged out successfully!');
                // Redirect to login page
                window.location.href = 'login.html';
            }
        }
    });
});

// Load job recommendations for the user
function loadJobRecommendations() {
    // For demo purposes, we'll use a mock user ID
    const userId = 1; // In a real app, this would come from authentication
    
    const resultsContainer = document.getElementById('job-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = '<p>Loading job recommendations...</p>';
    
    // Simulate API call with demo data
    setTimeout(() => {
        const demoJobs = [
            {
                title: "Senior Data Scientist",
                company: "TechCorp Inc.",
                location: "San Francisco, CA",
                salary_range: "$120,000 - $150,000",
                description: "Join our team to build cutting-edge machine learning models and drive data-driven decisions.",
                match_score: 0.92
            },
            {
                title: "Frontend Developer",
                company: "WebSolutions Ltd.",
                location: "New York, NY",
                salary_range: "$90,000 - $110,000",
                description: "Create beautiful, responsive web applications using modern JavaScript frameworks.",
                match_score: 0.78
            },
            {
                title: "UX Designer",
                company: "DesignHub",
                location: "Remote",
                salary_range: "$85,000 - $105,000",
                description: "Design intuitive user experiences for web and mobile applications.",
                match_score: 0.85
            },
            {
                title: "DevOps Engineer",
                company: "CloudTech",
                location: "Austin, TX",
                salary_range: "$110,000 - $130,000",
                description: "Implement and maintain scalable cloud infrastructure and CI/CD pipelines.",
                match_score: 0.88
            },
            {
                title: "Product Manager",
                company: "InnovateCo",
                location: "Seattle, WA",
                salary_range: "$100,000 - $125,000",
                description: "Lead product development from conception to launch, working with cross-functional teams.",
                match_score: 0.75
            },
            {
                title: "Cybersecurity Analyst",
                company: "SecureNet",
                location: "Washington, DC",
                salary_range: "$95,000 - $115,000",
                description: "Protect organizational assets by implementing security measures and monitoring for threats.",
                match_score: 0.82
            }
        ];
        
        displayRecommendedJobs(demoJobs.map(job => ({
            job: job,
            match_score: job.match_score
        })));
    }, 1500);
}

// Display recommended jobs with match scores
function displayRecommendedJobs(recommendations) {
    const resultsContainer = document.getElementById('job-results');
    
    if (!resultsContainer) return;
    
    if (!recommendations || recommendations.length === 0) {
        resultsContainer.innerHTML = '<p>No job recommendations found.</p>';
        return;
    }
    
    resultsContainer.innerHTML = recommendations.map(rec => {
        const job = rec.job;
        const matchScore = Math.round(rec.match_score * 100);
        
        return `
        <div class="job-card">
            <div class="job-header">
                <h3>${job.title || 'Job Title'}</h3>
                <span class="match-score">${matchScore}% Match</span>
            </div>
            <p class="company"><i class="fas fa-building"></i> ${job.company || 'Company Name'}</p>
            <p class="location"><i class="fas fa-map-marker-alt"></i> ${job.location || 'Location'}</p>
            <p class="salary"><i class="fas fa-dollar-sign"></i> ${job.salary_range || 'Salary Range'}</p>
            <p class="description">${job.description || 'Job description not available.'}</p>
            <div class="job-tags">
                <!-- Tags would be populated based on matched skills -->
                <span class="tag">Python</span>
                <span class="tag">Machine Learning</span>
                <span class="tag">SQL</span>
            </div>
            <div class="job-actions">
                <button class="btn primary-btn">Apply Now</button>
                <button class="btn secondary-btn">Save Job</button>
            </div>
        </div>
        `;
    }).join('');
}

// API utility functions
const API_BASE_URL = 'http://localhost:5000/api';

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// User authentication functions
async function registerUser(userData) {
    try {
        const response = await apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        return response;
    } catch (error) {
        console.error('Registration failed:', error);
        throw error;
    }
}

async function loginUser(credentials) {
    try {
        const response = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
        return response;
    } catch (error) {
        console.error('Login failed:', error);
        throw error;
    }
}

// Resume upload function
async function uploadResume(file, userId) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', userId);
        
        const response = await fetch(`${API_BASE_URL}/resumes/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Resume upload failed:', error);
        throw error;
    }
}

// Enhanced job card interaction
document.addEventListener('click', function(e) {
    // Handle job card clicks
    if (e.target.closest('.job-card') && !e.target.closest('.job-actions')) {
        const jobCard = e.target.closest('.job-card');
        jobCard.style.transform = 'scale(0.98)';
        setTimeout(() => {
            jobCard.style.transform = '';
        }, 150);
        console.log('Job card clicked');
    }
    
    // Handle save job button clicks
    if (e.target.classList.contains('secondary-btn') && e.target.textContent.includes('Save')) {
        const button = e.target;
        const originalText = button.textContent;
        button.textContent = 'Saved!';
        button.style.backgroundColor = '#4CAF50';
        button.style.borderColor = '#4CAF50';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '';
            button.style.borderColor = '';
        }, 2000);
    }
    
    // Handle profile menu clicks for mobile
    if (e.target.closest('.profile-menu ul li a')) {
        // Close mobile menu if open
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        if (hamburger && navMenu && hamburger.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    }
});