# Barangay Concerns

## Overview
A web-based Barangay Concern Management System that allows residents to submit, track, and manage barangay concerns online. It includes AI-powered assistance, real-time notifications, location tracking, analytics dashboards, and role-based access control for residents, staff, and administrators.

## Tech Stack
- **Django 4.2** – Backend web framework (Python)
- **PostgreSQL** – Production database
- **Google Gemini AI** – AI assistant for concern categorization and responses
- **Cloudinary** – Media and image storage
- **WhiteNoise + Gunicorn** – Static file serving and WSGI server
- **Render** – Cloud deployment platform

## Features
- 📝 Concern submission and tracking (with status updates)
- 🤖 AI-powered concern assistance via Google Gemini
- 🔐 Role-based login (Resident, Staff, Admin)
- 📊 Analytics dashboard for concern trends
- 🔔 Real-time notifications system
- 🗺️ Map view for location-tagged concerns
- 🛡️ Security management (user roles and permissions)
- 💬 Threaded comment and reply system on concerns

## Screenshots
> _Add screenshots of the app here (e.g., dashboard, concern form, map view)_

<!-- Example:
![Dashboard](screenshots/dashboard.png)
![Concern Form](screenshots/concern_form.png)
![Map View](screenshots/map_view.png)
-->

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (for production) or SQLite (for local dev)
- Git

### Steps to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/barangay_concerns.git
   cd barangay_concerns
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd barangay_concerns
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file inside the `barangay_concerns/` directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   GEMINI_API_KEY=your-gemini-api-key
   DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URL
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

### Deployment
This project is configured for deployment on **Render** using `render.yaml`. Set `GEMINI_API_KEY` manually in the Render dashboard environment variables.
