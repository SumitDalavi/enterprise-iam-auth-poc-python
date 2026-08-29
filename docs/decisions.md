# Decisions

## ADR-001: Short-Lived Access Tokens
**Date:** 2026-08-29  
**Status:** Accepted

**Context:**  
Enterprise IAM requires limiting the blast radius of stolen credentials. If we issue long-lived tokens, an attacker has sustained access.

**Decision:**  
We issue short-lived JWT access tokens (e.g., 30 mins) and require secure refresh tokens to maintain sessions.

**Consequences:**  
- ✅ Reduces window of vulnerability if a token is exfiltrated.
- ⚠️ Clients must implement refresh logic gracefully.
