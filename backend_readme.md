# Student Grievance Management System - Backend Documentation

This document provides a comprehensive overview of the backend architecture, logic, and data models for the Student Complaint and Grievance Management System.

## 1. Technology Stack
- **Framework**: Django 4.2.x (Python-based Web Framework)
- **Database**: SQLite 3 (Development/Default)
- **Auth**: Django Built-in Authentication System with a Custom User Model
- **Frontend-Backend Integration**: Django Templates (SSR) with Context-based Data Injection

---

## 2. Core Data Models

### User Model (`core.User`)
The system uses an extension of Django's `AbstractUser` to support role-based permissions and departmental assignments.
- **Roles**:
  - `student`: Standard access to submit and track own complaints.
  - `staff`: Officers assigned to resolve specific grievances.
  - `hod`: Head of Department; receives escalated cases from Staff.
  - `dean`: Senior administration; final escalation point for unresolved cases.
  - `admin`: Super-administrator with full system control.
- **Departments**: Academic, Hostel, Infrastructure, Admin, Other.

### Complaint Model (`core.Complaint`)
The central entity of the system.
- **Fields**:
  - `user`: ForeignKey to the Student.
  - `assigned_to`: ForeignKey to the Staff/Admin currently handling the case.
  - `title` & `description`: Core complaint content.
  - `category`: Matches departmental types for auto-routing.
  - `gender`: Used to filter relevant hostel options.
  - `location`: Specific MIT Manipal Hostel Block or Campus Area.
  - `status`: Pending, In Progress, Resolved, Escalated.
  - `escalation_level`: 0 (Staff), 1 (HOD), 2 (Dean).
  - `admin_remark`: Feedback provided by administrators.

---

## 3. Key Backend Logic

### A. Automatic Case Routing
When a student submits a complaint, the backend performs the following:
1. Identifies the **category** of the grievance (e.g., "Hostel").
2. Queries for all administrative users belonging to that **department**.
3. Selects the officer with the **lowest current workload** (number of active assigned complaints) to ensure balanced distribution.
4. If no department-specific officer is found, it falls back to a general administrator.

### B. Smart Location Filtering
The backend supports dynamic filtering of hostel locations based on student input.
- Locations are structured as grouped tuples (**optgroups**) in the model.
- A JavaScript layer interacts with the model-rendered `Select` widget to show only "Boys Hostels" or "Girls Hostels" based on the student's selected gender.

### C. Manual Escalation Workflow
Unlike standard time-based systems, this system empowers students to trigger escalations:
1. **Level 0 → 1**: If a student is unsatisfied with staff progress, they can escalate to the **HOD**.
2. **Level 1 → 2**: If still unresolved, the issue is moved to the **Dean**.
3. **Logic**: The backend reassigns the `assigned_to` field to an officer of the next higher rank in the same department during this process.

---

## 4. Administrative Control & RBAC
Access is strictly controlled via Django's `user_passes_test` and `login_required` decorators.
- **Student Dashboard**: Filtered to only show complaints submitted by `request.user`.
- **Admin Dashboard**:
  - **Super-admins**: See all complaints system-wide.
  - **Staff/HOD/Dean**: See complaints either directly assigned to them OR within their specific department.

---

## 5. Analytics Engine
The backend aggregates data for administrative oversight:
- **Concentration Heatmap**: Aggregates complaint counts by `location`.
- **Department Load**: A breakdown of grievances by `category`.
- **Leaderboard**: Ranks administrators based on their **Resolved Count**, encouraging operational efficiency.

---

## 6. Installation & Execution
1. **Environment Setup**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install django django-crispy-forms crispy-bootstrap5
   ```
2. **Database Migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Running the Server**:
   ```bash
   python manage.py runserver
   ```

---
*Documentation maintained by Antigravity AI.*
