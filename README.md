# 🎓 Student Complaint & Grievance Management System

A high-performance, full-stack web application designed to streamline student grievances through automated routing, SL tracking, and hierarchical escalation.

---

## 🚀 Key Features

### 👨‍🎓 Student Portal
- **Modern Dashboard**: Track complaints via a lifestyle-inspired interface.
- **Form Submission**: Categorized complaints (Academic, Hostel, Infrastructure, etc.) with location tracking.
- **SLA Countdown**: Transparent resolution timelines (48-hour initial window).

### 🧑‍💼 Administrative Console
- **Smart Auto-Routing**: Complaints automatically assigned based on department and workload balancing.
- **Hierarchical Escalation**: Automated progression from **Staff → HOD → Dean** for overdue cases.
- **Operational Analytics**: Real-time "Heatmap" and load distribution charts using **Chart.js**.
- **Performance Leaderboard**: Gamified admin ranking based on resolution rates.

### 🍱 UI/UX & Design
- **Glassmorphism**: Sleek, semi-transparent navigation and cards.
- **Responsive Layout**: Fully optimized for mobile and desktop using **Bootstrap 5**.
- **Smooth Animations**: Interactive transitions and micro-animations.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+ / Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, jQuery
- **Analytics**: Chart.js
- **Database**: SQLite3 (Standard) / MySQL Ready
- **Styling**: Custom CSS Design System

---

## 🏁 Quick Start

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Setup Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install django django-crispy-forms crispy-bootstrap5
```

### 3. Initialize Database
```bash
python manage.py makemigrations core
python manage.py migrate
```

### 4. Run Application
```bash
python manage.py runserver
```

---

## 🔑 Test Credentials (Seeded)

| Username | Role | Password |
| :--- | :--- | :--- |
| `admin` | Super Admin | `admin123` |
| `student` | Student | `student123` |
| `staff_acad` | Academic Staff | `staff123` |
| `hod_acad` | Academic HOD | `hod123` |
| `dean_office` | Dean | `dean123` |

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
