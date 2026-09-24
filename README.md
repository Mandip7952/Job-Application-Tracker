# Job Application Tracker

A full-stack web application for managing and tracking job applications in one place.

The application allows users to add, edit, delete, search, filter, and sort job applications while providing a dashboard with application statistics and upcoming deadlines.

## Features

- Add new job applications
- Edit existing applications
- Delete applications
- Search applications by company or job title
- Filter applications by status
- Sort applications by deadline
- Track application status
- View upcoming deadlines
- Dashboard with application statistics
- Application status chart
- Server-side input validation
- Responsive user interface

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- Git & GitHub

## Application Statuses

The tracker supports the following statuses:

- Saved
- Applied
- Assessment
- Interview
- Offer
- Rejected

## Dashboard

The dashboard provides:

- Total number of applications
- Number of applied applications
- Number of interviews
- Number of offers
- Number of rejected applications
- Upcoming application deadlines
- Application status visualization

## Project Structure

```text
Job-Application-Tracker/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── add_application.html
│   ├── applications.html
│   ├── base.html
│   ├── dashboard.html
│   ├── edit_application.html
│   └── index.html
│
├── .gitignore
├── app.py
└── README.md