# RFC-003: Replace OSRM with Google Maps Platform for Routing

**Status:** Under Review — Awaiting Hema Yadav (8 days)
**Author:** Avani Kshirsagar
**Date:** 2026-04-30

## Problem

Our self-hosted OSRM instance has:
- P95 route calculation latency: 380ms (target: <100ms)
- Infrastructure cost: $840/month for the OSRM server
- Missing: real-time traffic, road closures, construction zones
- Incident: 3 driver routes through closed road in April

## Proposal

Migrate to Google Maps Platform Directions API:
- P95 latency: ~45ms (Google SLA)
- Real-time traffic data included
- Pricing: ~$5 per 1000 requests (~$400/month at current volume)

## Decision Criteria

| Criterion | OSRM (current) | Google Maps |
|-----------|----------------|-------------|
| Latency | 380ms | ~45ms |
| Traffic awareness | ❌ | ✅ |
| Cost/month | $840 | ~$400 |
| Offline capability | ✅ | ❌ |
| SLA | None | 99.9% |

## Open Questions (Identified by Resonance RFC Reviewer)

- ❌ **Missing: Failure mode analysis** — What happens when Google Maps API
  is unavailable? OSRM was our fallback. What's the fallback for Google Maps?

- ❌ **Missing: Cost projection** — The $400/month estimate assumes current
  volume. What's the projection at 10× growth? At surge peak (300 req/min)?

- ❌ **Missing: Rollback plan** — If we migrate and Google Maps degrades our
  matching quality, how do we roll back? Is OSRM kept warm?

## Recommendation (Resonance analysis)

Do not approve until failure modes and rollback plan are documented.
The latency and cost improvements are compelling, but a dependency on
a single external routing provider is a platform risk for a safety-critical
feature (SOS trip sharing uses the route).
