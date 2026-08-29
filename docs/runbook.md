# Runbook — enterprise-iam-auth-poc-python
> Last updated: 2026-08-29

## Prerequisites
| Tool | Required Version | How to check |
|---|---|---|
| Docker & Compose | Latest | `docker-compose version` |

## Quick Start
```bash
# Start service
docker-compose up -d --build

# Open Swagger UI
# http://localhost:8080/docs
```

## Run Tests
```bash
# Run pytest locally
pytest tests/

# Run OIDC Federation test script
bash tests/e2e/test_oidc_federation.sh
```

## Environment Variables
| Variable | Default | Purpose |
|---|---|---|
| SECRET_KEY | `your-super-secret-key...` | Used to sign JWTs |
| ALGORITHM | `HS256` | JWT signing algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES| `30` | JWT expiration |

## Common Failure Modes
| Symptom | Cause | Fix |
|---|---|---|
| 401 Unauthorized | Token expired | Re-authenticate or use refresh token |
