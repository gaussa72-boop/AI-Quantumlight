# Quantum Payments & Credits

Shared prepaid-credit contract. Verified idempotent payment events only; provider adapters for Stripe/crypto; no private keys/custody. Production ledger state must be persistent and transactional. Paid generation should reserve credits before work and release them on failure. Secrets must remain in deployment secret storage.
