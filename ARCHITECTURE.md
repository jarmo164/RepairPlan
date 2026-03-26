# RepairPlan Architecture

## Overview

RepairPlan is a web-based repair work management system built to replace an Excel-driven workflow with a structured, role-based application.

The system is intended for:
- Department managers
- Repair master
- Repair technicians
- Administrators

Its core purpose is to centralize repair intake, assignment, prioritization, status tracking, and reporting.

---

## Chosen Architecture Direction

RepairPlan will use an **API-first architecture**:
- **Backend:** Django + Django REST Framework
- **Frontend:** separate client consuming the API
- **Database:** SQLite for development, PostgreSQL for production

This means the backend is responsible for:
- authentication
- authorization
- business rules
- workflow validation
- auditability
- filtered data access by role

The frontend is responsible for:
- presenting the workflow
- calling the API
- rendering role-appropriate actions based on API capabilities and user state

---

## Why REST API First

The decision to use REST is not because authentication is simpler — it is not. The reason is architectural flexibility.

This direction is justified when we want:
- a cleaner backend/frontend separation
- easier future mobile support
- easier future integrations with other systems
- a reusable API surface for multiple clients
- a system that can grow beyond a single server-rendered web UI

The cost is higher implementation complexity up front, but the payoff is greater long-term flexibility.

---

## Recommended Tech Stack

### Backend
- **Django**
- **Django REST Framework**
- **Django built-in authentication**
- **Django Groups + permission checks**
- optional token/session strategy depending on frontend integration approach

### Database
- **SQLite** for development
- **PostgreSQL** for production

### Frontend
- separate frontend application
- exact framework can remain open for now, but the backend should expose clean REST endpoints from day one

---

## Architecture Principles

### 1. API-first, but not logic-in-views
Business logic must not be scattered across DRF views/viewsets/serializers.

Recommended separation:
- `models.py` → data model
- `serializers.py` → transport/input-output schemas
- `views.py` → endpoint handling
- `selectors.py` → filtered/read-side query logic
- `services.py` → state changes, assignments, audit logging
- `permissions.py` → central role and access rules

### 2. Backend is the source of truth
The frontend can hide or show buttons, but the backend must strictly enforce:
- who can view which records
- who can edit which records
- who can assign repairers
- who can change status and priority
- which workflow transitions are allowed

### 3. Domain-first design
The repair workflow is the real system. API endpoints should reflect domain needs, not random CRUD for its own sake.

### 4. Build for growth without premature fragmentation
This should still be one backend application with clear internal structure, not a distributed microservice mess.

---

## Suggested Project Structure

```text
repairplan/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── repairs/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── permissions.py
│   ├── selectors.py
│   ├── services.py
│   └── tests/
├── templates/
│   └── registration/
├── requirements.txt
└── README.md
```

Notes:
- `templates/registration/` may still exist if Django-admin or server-side login screens are used for internal auth flows.
- the user-facing workflow UI is expected to live in a separate frontend client.

---

## Domain Model

### Repair
Primary entity representing a repair item.

Suggested fields:
- `id`
- `product_code`
- `quantity`
- `client_or_group`
- `department`
- `created_at`
- `created_by`
- `priority`
- `status`
- `assigned_to`
- `comment`
- `updated_at`

### RepairComment
Separate model for timeline comments.

Suggested fields:
- `repair`
- `author`
- `comment`
- `created_at`

### RepairStatusLog
Tracks important workflow changes for auditing.

Suggested fields:
- `repair`
- `changed_by`
- `field_name`
- `old_value`
- `new_value`
- `created_at`

### Department
Should be a dedicated model instead of a plain text field.

Why:
- cleaner filtering
- stronger reporting
- easier permission mapping
- less duplicated data

### UserProfile
Attach business metadata to users, especially department membership.

Suggested fields:
- `user`
- `department`
- optional role-related metadata if needed later

**Recommendation:** use `UserProfile` instead of a custom Django user model for v1 unless there is a clear auth-level requirement to replace Django's default user.

---

## Enums and Controlled Values

### Repair Status
Suggested internal values:
- `NOT_STARTED`
- `REVIEWED`
- `IN_PROGRESS`
- `ON_HOLD`
- `COMPLETED`
- `RETURNED`

### Priority
Suggested internal values:
- `HIGH`
- `MEDIUM`
- `LOW`

API responses can expose human-readable labels alongside stable internal values if useful.

---

## Roles and Permissions

Recommended Django Groups:
- `department_manager`
- `repair_master`
- `repairer`
- `administrator`

### Department Manager
Can:
- create repair entries
- view entries from their own department
- open detail views for their department’s records

Cannot:
- assign repairers
- manage system-wide workflow beyond allowed scope
- view other departments’ work

### Repair Master
Can:
- view all repairs
- set priority
- change status
- assign repairers
- add comments
- access dashboard/reporting endpoints

### Repairer
Can:
- view only repairs assigned to them
- update status within allowed workflow transitions
- add comments

Cannot:
- browse all repairs
- edit work assigned to others

### Administrator
Can:
- manage users
- manage groups and permissions
- access the whole system
- use Django admin

---

## API Design Direction

Suggested endpoint groups:

### Auth / session
- `POST /api/auth/login/` or session-based equivalent
- `POST /api/auth/logout/`
- `GET /api/auth/me/`

### Repairs
- `GET /api/repairs/`
- `POST /api/repairs/`
- `GET /api/repairs/{id}/`
- `PATCH /api/repairs/{id}/`

### Repair workflow actions
- `POST /api/repairs/{id}/assign/`
- `POST /api/repairs/{id}/change-status/`
- `POST /api/repairs/{id}/change-priority/`

### Comments
- `GET /api/repairs/{id}/comments/`
- `POST /api/repairs/{id}/comments/`

### Dashboard / reporting
- `GET /api/dashboard/summary/`
- `GET /api/repairs/my-work/`
- `GET /api/repairs/export/`

This does **not** mean everything must be a generic ViewSet. Domain actions deserve explicit endpoints when they improve clarity.

---

## Workflow Design

Suggested allowed status transitions:
- `NOT_STARTED` → `REVIEWED`
- `REVIEWED` → `IN_PROGRESS`
- `IN_PROGRESS` → `ON_HOLD`
- `ON_HOLD` → `IN_PROGRESS`
- `IN_PROGRESS` → `COMPLETED`
- `REVIEWED` → `RETURNED`
- `IN_PROGRESS` → `RETURNED`

Rules:
- repairers should only be allowed to make limited transitions on their own assigned work
- repair masters can apply all business-approved transitions
- all major changes should be logged
- transition validation should live in the service layer, not be duplicated across serializers and views

---

## Frontend Expectations

Because the frontend is separate, it should assume:
- all business-critical permission checks happen on the backend
- filtered list endpoints return only what the user may see
- the API may expose metadata for allowed actions if needed later
- UI role restrictions are convenience, not security

---

## Security and Data Integrity

Required baseline:
- authenticated access for all write operations
- secure auth/session/token strategy
- CSRF protection where applicable
- server-side validation
- strict queryset filtering by role and department
- audit logging for important changes
- admin access restricted to authorized roles only

---

## Scalability Considerations

Recommended preparation:
- PostgreSQL in production
- indexes for `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination on list endpoints
- service layer for future notifications
- optional async/background jobs later (Celery or RQ)
- API versioning only when real change pressure appears

---

## Final Recommendation

The chosen path for RepairPlan is:
1. Django + DRF backend
2. Separate frontend client
3. Department + UserProfile + Repair + Comment + StatusLog domain model
4. Django Groups and backend permission enforcement
5. SQLite for development, PostgreSQL for production
6. Audit logging and CSV export in the first serious version

This increases initial complexity compared to server-rendered templates, but it gives the project a cleaner path toward multiple clients and future integrations.
