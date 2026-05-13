# ADR-005: Shared Database Connection Pool

**Status:** Proposed — Awaiting Review (8 days)
**Author:** Avani Kshirsagar
**Date:** 2026-04-28
**Reviewers:** Hema Yadav (pending), Mahindra Kshirsagar

## Context

The matching-service and payments-service currently maintain separate
PostgreSQL connection pools. Under surge conditions (>300 concurrent
rides), we're hitting connection limit errors on both pools simultaneously.
The database server supports 500 max connections; we're using 480 at peak.

## Decision

**Proposed:** Share a single PgBouncer connection pool between matching-service
and payments-service, managed by a new `db-proxy` sidecar.

## Consequences

**Positive:**
- Reduces peak connection usage from 480 → ~240
- Simplifies connection management
- Lower database infrastructure cost

**Negative:**
- Creates a shared dependency between two services
- A misconfigured query in one service could starve the other
- Violates service boundary principle (services should own their data)

## Alternatives Considered

1. Increase RDS instance size (expensive, doesn't solve root cause)
2. Implement connection pooling per service with PgBouncer (preferred by Hema)
3. Move to async message queue for cross-service communication (longer term)

## Open Questions

- [ ] What happens when matching-service floods the pool during surge?
- [ ] Rollback plan if db-proxy fails?
- [ ] How do we isolate connection budgets per service?

**⚠️ This ADR needs Hema's input on the service boundary implications.**
