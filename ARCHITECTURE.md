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

## Recommended Tech Stack

- **Backend:** Django
- **Database:** SQLite for development, PostgreSQL for production
- **Frontend:** Django Templates + Bootstrap 5
- **Authentication:** Django built-in auth
- **Authorization:** Django Groups + server-side permission checks
- **Auditability:** Dedicated status/change log model
- **Export:** CSV initially, Excel later if needed

### Why this stack

This project does not need a frontend-heavy SPA architecture. Django provides:
- mature authentication and admin tools
- fast CRUD development
- robust ORM and forms
- strong maintainability for internal business systems

Using Django templates keeps complexity low while still delivering a reliable production-ready UI.

---

## Architecture Principles

### 1. Start as a structured monolith
A monolith is the right choice here. The domain is operational workflow management, not distributed computing.

### 2. Keep domain boundaries clear
Even inside a monolith, application logic should not be dumped into views.

Recommended separation:
- `models.py` → data model
- `views.py` → request/response handling
- `forms.py` → input validation and form shaping
- `selectors.py` → filtered/read-side query logic
- `services.py` → state changes, assignments, audit logging
- `permissions.py` → central role and access rules

### 3. Enforce permissions on the server
UI hiding is not security. Every list, detail view, and mutation must be permission-aware on the backend.

### 4. Design for growth without overengineering
The first version should be simple, but it must leave room for:
- notifications
- reporting
- exports
- future API integrations

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
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── permissions.py
│   ├── selectors.py
│   ├── services.py
│   └── tests/
├── templates/
│   ├── base.html
│   ├── registration/login.html
│   └── repairs/
├── static/
│   └── css/
├── requirements.txt
└── README.md
```

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

**Recommendation:** use `UserProfile` instead of a custom Django user model for v1.

---

## Enums and Controlled Values

### Repair Status
Internal values should be stable English constants, while the UI can show Estonian labels.

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

This avoids future migration pain if UI text changes.

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
- access dashboard and reporting views

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

---

## Main Views

### Authentication
- login
- logout
- optional password management later

### Repair List
Features:
- search by product code
- filter by department
- filter by client/group
- filter by status
- filter by priority
- filter by assigned repairer
- sort by created date
- paginated table view

### Create Repair
Simple, fast intake form for department managers.

Automatically set:
- `created_by`
- `created_at`

### Repair Detail
Shows:
- main record data
- current assignment
- comments
- status log / history
- contextual actions depending on user role

### Repair Edit
Behavior depends on role:
- department manager → limited editing scope
- repair master → full business editing scope
- repairer → only work-related updates allowed

### My Work
Dedicated repairer view showing only assigned work.

### Dashboard
For repair master / administrators.

Should include:
- count of not started repairs
- count of in-progress repairs
- count of completed repairs
- count of high-priority repairs
- oldest open repairs
- repair counts grouped by assigned technician

---

## UI / UX Direction

This should feel like a dependable internal operations tool, not a flashy demo product.

### Principles
- clear navigation
- table-first workflow
- simple forms
- fast scanning
- clear visual state labels

### Styling
- Bootstrap 5 base
- badge colors for priority and status
- practical spacing and dense-enough data layouts
- mobile support is useful, but desktop-first is the correct default

Suggested badge colors:
- Not started → gray
- Reviewed → blue
- In progress → orange
- On hold → dark/neutral
- Completed → green
- Returned → red

---

## Security and Data Integrity

Required baseline:
- authenticated access for all write operations
- CSRF protection
- server-side validation
- strict queryset filtering by role and department
- audit logging for important changes
- admin access restricted to authorized roles only

---

## Scalability Considerations

Not “big tech scale” — just sane growth planning.

Recommended preparation:
- PostgreSQL in production
- indexes for `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination on list views
- service layer for future notifications
- optional async/background jobs later (Celery or RQ)
- future REST API only if real integration needs appear

---

## Delivery Plan

### Phase 1 — Project Skeleton
- initialize Django project
- create `repairs` app
- configure templates, static files, auth, Bootstrap base layout

### Phase 2 — Data Model
- Department
- UserProfile
- Repair
- RepairComment
- RepairStatusLog
- admin configuration
- migrations

### Phase 3 — Roles and Permission Layer
- Django Groups
- permission helpers
- filtered selectors/querysets
- restricted access by role

### Phase 4 — Core Workflow Views
- repair list
- create repair
- repair detail
- repair update
- my work view

### Phase 5 — Dashboard
- KPI summary cards
- oldest open repairs
- counts by repairer

### Phase 6 — Audit, Comments, Export
- timeline comments
- change logs
- CSV export

### Phase 7 — Hardening
- permission tests
- form tests
- core view tests
- README run instructions
- UX polish

---

## MVP Scope

Recommended MVP includes:
- login
- roles
- repair creation
- repair list with filters
- detail view
- my work view
- master dashboard
- comments
- basic audit logging

Can be deferred:
- email notifications
- Excel export
- public API
- realtime updates
- complex workflow engine

---

## Final Recommendation

The best implementation path is:
1. Django monolith
2. Django templates + Bootstrap UI
3. Department + UserProfile + Repair + Comment + StatusLog
4. Django Groups for roles
5. SQLite for dev, PostgreSQL for production
6. CSV export and audit logging in the first serious version

This keeps the system maintainable, production-sensible, and fast to build without turning a straightforward operational app into accidental architecture cosplay.
