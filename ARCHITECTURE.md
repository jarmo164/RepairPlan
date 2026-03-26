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

RepairPlan will use a **hybrid server-rendered architecture**:
- **Backend:** Django
- **UI rendering:** Django Templates
- **Dynamic data loading:** vanilla JavaScript via `fetch`
- **API layer:** internal REST-style endpoints for table data, detail fragments, workflow actions, summaries, and exports
- **Database:** SQLite for development, PostgreSQL for production

This is **not** a SPA architecture.

The application uses:
- server-rendered HTML for the main shell and page structure
- client-side enhancement for dynamic updates
- backend-enforced permissions and workflow rules

This gives us a practical middle ground:
- simpler than React/Vue SPA architecture
- more dynamic than purely static server-rendered CRUD pages
- well suited for internal business systems

---

## Why This Direction

This architecture is a good fit because it provides:
- fast development speed
- a clear and maintainable permission model
- no unnecessary frontend build complexity
- reusable API endpoints for dynamic UI behavior
- a robust user experience for internal operational workflows

Instead of building a separate frontend client, we keep the app as one coherent Django system while still exposing structured data endpoints where the UI benefits from async loading.

---

## Recommended Tech Stack

### Backend
- **Django**
- **Django REST Framework** or focused Django JSON endpoints
- **Django built-in authentication**
- **Django Groups + permission checks**

### Database
- **SQLite** for development
- **PostgreSQL** for production

### Frontend
- **Django Templates**
- **Bootstrap**
- **Icon library**
- **Vanilla JavaScript**
- **Shared fetch-based API wrapper**
- **Chart.js** when charts are needed

---

## Frontend Rendering Model

The UI follows the pattern:

**server-rendered skeleton + client-side enrichment**

That means:
1. Django renders the page shell, layout, navigation, and base structure.
2. The browser loads a shared JS layer.
3. Specific sections fetch additional data from API endpoints.
4. The DOM is updated in-place for tables, summaries, status widgets, comments, or charts.

Examples:
- a list page renders filters and table shell server-side, then loads rows via API
- a dashboard renders layout and KPI placeholders server-side, then loads metrics and charts asynchronously
- a detail page renders the base record shell and action areas, then updates comments/history dynamically

---

## Layout and UI Structure

All pages should share a common base template containing:
- top navigation bar
- messages/alerts area
- global loading indicator
- shared script includes
- shared UI components
- role-aware navigation state

Expected reusable UI pieces:
- filter bar
- table shell
- pagination block
- status badges
- priority badges
- modal structure
- empty states
- inline feedback messages

---

## Shared JavaScript Layer

A common JavaScript layer should provide:
- `GET/POST/PATCH/DELETE` helpers
- automatic JSON request/response handling
- automatic CSRF header injection for write operations
- centralized error handling
- global loading state integration
- reusable DOM update helpers where practical

This avoids page-level script chaos.

---

## Architecture Principles

### 1. Server-render first, enrich second
The system should work from a clear server-rendered page structure, then add dynamic behavior where it improves UX.

### 2. Backend is the source of truth
The frontend can hide or show buttons, but the backend must strictly enforce:
- who can view which records
- who can edit which records
- who can assign repairers
- who can change status and priority
- which workflow transitions are allowed

### 3. Domain-first design
The repair workflow is the real system. Templates, endpoints, and services should reflect domain actions, not random CRUD scatter.

### 4. Keep logic out of templates and thin out views
Do not dump business logic into templates or into fat Django/DRF views.

Recommended separation:
- `models.py` → data model
- `forms.py` → server-rendered form logic
- `serializers.py` → JSON transport schemas where needed
- `views.py` → HTML views and/or API views
- `selectors.py` → filtered/read-side query logic
- `services.py` → state changes, assignments, audit logging
- `permissions.py` → central role and access rules

### 5. Avoid accidental frontend framework reimplementation
If the JS layer starts behaving like a poor homemade SPA, we have gone too far.

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
│   ├── forms.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── permissions.py
│   ├── selectors.py
│   ├── services.py
│   └── tests/
├── templates/
│   ├── base.html
│   ├── registration/
│   └── repairs/
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
└── README.md
```

Suggested JS structure:

```text
static/js/
├── api.js
├── ui.js
├── loading.js
├── repairs-list.js
├── repair-detail.js
└── dashboard.js
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

JSON responses can expose human-readable labels alongside stable internal values if useful.

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
- access dashboard/reporting views and related data endpoints

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

## View and Endpoint Design Direction

The system should combine:
- **HTML page views** for main navigation targets
- **JSON endpoints** for async data loading and workflow actions

Suggested page views:
- login
- repair list page
- create repair page
- repair detail page
- repair edit page
- my work page
- dashboard page

Suggested data/action endpoints:
- `GET /api/repairs/`
- `POST /api/repairs/`
- `GET /api/repairs/{id}/`
- `PATCH /api/repairs/{id}/`
- `POST /api/repairs/{id}/assign/`
- `POST /api/repairs/{id}/change-status/`
- `POST /api/repairs/{id}/change-priority/`
- `GET /api/repairs/{id}/comments/`
- `POST /api/repairs/{id}/comments/`
- `GET /api/dashboard/summary/`
- `GET /api/repairs/my-work/`
- `GET /api/repairs/export/`

This does **not** mean every page must be empty HTML waiting for JS. The page shell should remain useful and understandable even before enrichment finishes.

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
- transition validation should live in the service layer, not be duplicated across templates and endpoints

---

## Security and Data Integrity

Required baseline:
- authenticated access for all write operations
- CSRF protection for write requests
- server-side validation
- strict queryset filtering by role and department
- audit logging for important changes
- admin access restricted to authorized roles only
- JS convenience must never replace backend permission enforcement

---

## Scalability Considerations

Recommended preparation:
- PostgreSQL in production
- indexes for `status`, `priority`, `created_at`, `assigned_to`, `department`
- pagination on list views and list endpoints
- service layer for future notifications
- optional async/background jobs later (Celery or RQ)
- keep API endpoints coherent enough to support future integrations if needed

---

## Final Recommendation

The chosen path for RepairPlan is:
1. Django server-rendered application
2. Bootstrap-based UI with shared base template
3. Vanilla JS enrichment with shared fetch wrapper
4. Internal JSON/REST-style endpoints for dynamic parts
5. Department + UserProfile + Repair + Comment + StatusLog domain model
6. Django Groups and backend permission enforcement
7. SQLite for development, PostgreSQL for production
8. Audit logging and CSV export in the first serious version

This gives the project a practical, maintainable architecture without dragging in a heavyweight SPA stack.
