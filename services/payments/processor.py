# feature/stripe-integration

# Auto-generated branch for ride-hailing platform

# Commit 1: feat(payments): add Stripe PaymentIntent capture flow

# Commit 2: feat(payments): implement webhook handler for payment events

# Commit 3: feat(payments): add idempotency key on payment retry

# Avani: add webhook signature verification
import hmac, hashlib

# Avani: idempotency key TTL set to 24h to prevent replay attacks
IDEMPOTENCY_TTL_SECS = 86400
# Avani: webhook signature
import hmac, hashlib
