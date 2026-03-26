# RepairPlan Deployment Notes

## Environment-based configuration

RepairPlan now supports environment-based configuration for:
- secret key
- debug flag
- allowed hosts
- SQLite vs PostgreSQL database selection
- email delivery settings
- notification toggle

Use `.env.example` as a reference.

## PostgreSQL

To use PostgreSQL in production, set:
- `DATABASE_ENGINE=postgres`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

## Background jobs

Current notification hooks are synchronous and lightweight.
If real production email volume grows, the next sensible step is:
- **Celery** if broader async workflow/queueing needs appear
- **RQ** if we want a simpler Redis-backed job queue

Current recommendation:
- do **not** add Celery or RQ yet
- add queueing only when real operational need appears


## Current notification behavior

Notifications are sent only on real state changes:
- assignment email only when assignee changes
- status email only when status changes

This avoids duplicate mail on idempotent updates.
