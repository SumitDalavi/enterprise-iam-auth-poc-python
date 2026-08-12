# Enterprise IAM & Auth Service PoC (Python) 🔐

> A modular Identity and Access Management (IAM) and Single Sign-On (SSO) service built with FastAPI, demonstrating enterprise-grade security patterns.

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

## 👨‍💻 Author

*Built to demonstrate enterprise Identity and Access Management patterns.*
