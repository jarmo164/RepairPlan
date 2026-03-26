# RepairPlan Integrations and Extension Notes

## API need assessment

Current system architecture already exposes internal JSON/REST-style endpoints for the web UI.
That is enough for the current product stage.

### When external API expansion becomes justified
External-facing or integration-oriented API work should be prioritized only when at least one of these becomes real:
- ERP / warehouse / CRM integration request
- mobile app requirement
- reporting export consumed by another system
- partner or internal platform wants machine-readable repair data

Until then, keep the API primarily optimized for the web application itself.

## Reporting expansion policy

Do not build many extra reports pre-emptively.
Add them only when an actual operational question repeats often, for example:
- backlog by department over time
- average turnaround time
- technician load distribution
- high-priority aging report

## `client_or_group` normalization

Current recommendation:
- keep `client_or_group` as a text field for now

Normalize it into a dedicated model only when at least one of these appears:
- repeated spelling/data consistency problems
- need for master-data management
- reporting grouped by normalized entity
- external integration depends on stable client/group IDs

## Integration design rule

When new integrations are added later:
- do not leak business logic into integration-specific code
- keep workflow validation in `services.py`
- keep filtering and visibility rules in `selectors.py` / permission layer
- prefer additive endpoints over breaking changes
