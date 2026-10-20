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

## ADR-002: Progressive Credential Loading (PCL) Architecture
- **Context:** Production hardening required live backends (PostgreSQL, Redis, OpenAI, Anthropic), but removing mocks would break CI pipelines and create high developer onboarding friction.
- **Decision:** Implement Progressive Credential Loading. Keep in-memory and local mock heuristics as the default safe baseline, while wrapping external integrations in auto-promoting factory adapters triggered by environment variables.
- **Consequences:** 
  - *Pros:* 100% CI pass rate without requiring external secrets; zero setup friction for new contributors; progressive upgrade to production clusters.
  - *Cons:* Adds lightweight factory abstraction layers and runtime credential detection logic.
