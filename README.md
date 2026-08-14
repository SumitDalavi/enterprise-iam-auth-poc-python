# Enterprise IAM & Auth Service PoC (Python) 🔐

> A modular Identity and Access Management (IAM) and Single Sign-On (SSO) service built with FastAPI, demonstrating enterprise-grade security patterns.

> **⚠️ PoC Note:** SSO endpoints use simulated OAuth2/OIDC flows (not connected to a real IdP like Okta or Azure AD). All auth logic (JWT, RBAC, password hashing) is fully functional.


> **🔗 See also:** [Node.js/TypeScript implementation](https://github.com/SumitDalavi/enterprise-iam-auth-poc-node) of the same IAM service — demonstrating polyglot capability across Python and Node.js ecosystems.


## The Problem

Most simple apps use basic JWTs and tightly couple their user authentication with their core business logic. In enterprise environments, Identity must be a centralized, secure service capable of handling complex RBAC (Role-Based Access Control), SSO (Single Sign-On), and secure token lifecycles without leaking credentials to downstream microservices.

## The Solution

This PoC separates Identity into a standalone service. It provides:
1. **SSO Simulation**: OAuth2/OIDC patterns with authorization codes and token exchanges.
2. **Enterprise RBAC**: Decoupled role and permission management.
3. **Secure Token Issuance**: Short-lived access tokens and secure refresh token handling.

By keeping identity decoupled, downstream services only need to validate the cryptographic signature of the token, allowing the architecture to scale securely.

## Why This Over the Obvious Alternative

Many developers just use Firebase Auth or Auth0 without understanding the underlying OAuth2/OIDC flows. Building this custom IAM service demonstrates a deep understanding of token lifecycles, asymmetric cryptography (simulated here with robust JWT signing), and proper separation of concerns in a Zero Trust architecture.

## 🛠️ Tech Stack

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Security**: PyJWT, Passlib (Bcrypt)
- **Containerization**: Docker

## Decision Log

| Decision | Rationale |
|----------|-----------|
| FastAPI | Provides built-in OAuth2 password and bearer token support, auto-generating compliant Swagger docs. |
| Decoupled RBAC | Roles are mapped to permissions dynamically rather than hardcoding scopes into user records, mimicking enterprise Active Directory/LDAP patterns. |
| Short-lived Access Tokens | Reduces the attack surface if a token is intercepted; relies on secure refresh mechanisms. |

## 🚀 Getting Started

```bash
docker-compose up -d --build
```
Access the interactive Swagger UI at `http://localhost:8000/docs`.

## 📁 Project Structure

For a detailed breakdown of the codebase and technical design decisions, please refer to the [Architecture Documentation](docs/ARCHITECTURE.md).


## 📋 Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://www.docker.com/) | >= 24.x | Container runtime |
| [Docker Compose](https://docs.docker.com/compose/) | >= 2.x | Multi-container orchestration |
| [curl](https://curl.se/) or browser | Any | API testing |

*For local dev without Docker: Python >= 3.11, pip*

## 🚀 Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/SumitDalavi/enterprise-iam-auth-poc-python.git
cd enterprise-iam-auth-poc-python

# 2. Build and start
docker-compose up -d --build

# 3. Verify it's running
curl http://localhost:8080/docs
```

The API and Swagger UI are now available at **http://localhost:8080/docs**

## 🧪 Usage & Demo â€” Full Auth Flow

### Step 1: Register a new user
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "SecureP@ss123"}'
```

### Step 2: Login to get a JWT token
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=SecureP@ss123"
# Response: {"access_token": "eyJhbGci...", "token_type": "bearer"}
```

### Step 3: Access protected endpoints
```bash
# Get current user info (any authenticated user)
curl http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer <TOKEN>"

# Access admin-only dashboard (RBAC-protected)
curl http://localhost:8080/api/v1/admin/dashboard \
  -H "Authorization: Bearer <TOKEN>"
```

### Step 4: SSO Simulation
```bash
# Initiate mock SSO authorization
curl http://localhost:8080/api/v1/sso/authorize

# Exchange code for token
curl -X POST http://localhost:8080/api/v1/sso/token \
  -H "Content-Type: application/json" \
  -d '{"code": "mock_authorization_code"}'
```

### Interactive Testing
Open **http://localhost:8080/docs** in your browser for the full Swagger UI where you can test all endpoints interactively.

## ✅ Verification

| Check | Command | Expected |
|-------|---------|----------|
| Swagger UI | Open `http://localhost:8080/docs` | Interactive API docs |
| Register | POST `/api/v1/auth/register` | 201 Created |
| Login | POST `/api/v1/auth/login` | JWT token returned |
| Auth Check | GET `/api/v1/users/me` with token | User info returned |
| RBAC | GET `/api/v1/admin/dashboard` | 200 for admin, 403 for user |

```bash
# Stop the service
docker-compose down
```

## 👨‍💻 Author

**Sumit Dalavi** — Senior DevSecOps / Platform Engineer
[GitHub](https://github.com/SumitDalavi) | [LinkedIn](https://in.linkedin.com/in/sumit-dalavi-762838129)

---

*Built with a focus on production-grade patterns, not toy demos.*