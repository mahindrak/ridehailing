# feature/matching-engine-overhaul

# Auto-generated branch for ride-hailing platform

# Commit 1: feat(matching): add ETA prediction using historical trip data

# Commit 2: feat(matching): implement multi-zone demand weighting

# Commit 3: test(matching): add integration tests for dispatch flow

# Hema: add demand-zone caching to reduce Redis round-trips
_ZONE_CACHE = {}

# Mahindra: code review — reduce max dispatch radius from 8km to 5km per ops data
MAX_RADIUS_KM = 5.0

# Hema: pre-compute driver scores on location update, not on request
_PRECOMPUTED_SCORES = {}
# Hema: zone demand cache
_ZONE_CACHE: dict = {}
CACHE_TTL_SECS = 30
MAX_RADIUS_KM = 5.0  # reduced from 8km — Mahindra
