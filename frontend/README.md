# Frontend

The frontend for Scopira is built with HTML, CSS, and JavaScript, providing a responsive user interface for all platform features.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open `http://localhost:8000` in your browser

## Pages

### Home (`index.html`)
- Landing page with platform overview
- Feature highlights
- Call-to-action buttons

### Dashboard (`dashboard.html`)
- User dashboard with skill visualizations
- Job match scores
- Recent activity feed
- Recommendations

### Jobs (`jobs.html`)
- Job search and filtering
- Job listings with match scores
- Job details and application

### Portfolio (`portfolio.html`)
- Interactive portfolio showcase
- Skills, projects, and experience
- Certifications and achievements

### Profile (`profile.html`)
- User profile management
- Resume upload and management
- Skill editing
- Job preferences

## Components

### Navigation
- Responsive navbar with mobile menu
- Page routing
- User authentication status

### Forms
- Registration and login forms
- Profile editing forms
- Resume upload form
- Job search filters

### Visualizations
- Skill radar charts (Chart.js)
- Job match bar charts (Chart.js)
- Interactive portfolio elements

## Project Structure

```
frontend/
├── index.html          # Landing page
├── dashboard.html      # User dashboard
├── jobs.html           # Job listings
├── portfolio.html      # Portfolio showcase
├── profile.html        # User profile
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── main.js         # Main JavaScript file
├── assets/             # Images and other assets
├── package.json        # NPM package file
└── README.md           # This file
```

## JavaScript Modules

### API Utilities
- `apiCall()` - Generic API call function
- `registerUser()` - User registration
- `loginUser()` - User login
- `uploadResume()` - Resume upload

### Form Validation
- `validateResumeUpload()` - Resume file validation

### UI Components
- `initDashboard()` - Initialize dashboard charts
- `searchJobs()` - Job search functionality
- Mobile navigation toggle

## Styling

The platform uses a modern, responsive design with:
- CSS Grid and Flexbox layouts
- Mobile-first approach
- Consistent color scheme
- Accessible typography
- Smooth animations and transitions