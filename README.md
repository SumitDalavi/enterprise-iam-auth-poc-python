# Enterprise IAM & Auth Service PoC 🔐

A comprehensive Proof of Concept demonstrating an Enterprise-Grade Identity and Access Management (IAM) Service built with **FastAPI**.

## 📖 Overview

Identity and Access Management is a critical component of any enterprise architecture. This PoC demonstrates the fundamental building blocks of a modern, secure, and modular authentication service. It utilizes Domain-Driven Design (DDD) to separate concerns such as core security, authentication, and Role-Based Access Control (RBAC).

## ✨ Enterprise Features

- **JWT (JSON Web Tokens)**: Secure, stateless token generation and validation.
- **RBAC (Role-Based Access Control)**: Granular endpoint protection using FastAPI dependencies.
- **Password Security**: State-of-the-art `bcrypt` password hashing via `passlib`.
- **SSO Simulation**: Mock federated login flows simulating OAuth2/OIDC (e.g., "Login with Google/Okta").
- **Modular Architecture**: Clean separation of `auth`, `sso`, and `rbac` domains.
- **Database Integration**: SQLAlchemy ORM backed by SQLite (easily swappable to PostgreSQL).

## 🚀 Getting Started

### Running with Docker (Recommended)

1. **Build and start the container**:
   ```bash
   docker-compose up -d --build
   ```
2. **Access the API**: 
   The service will be running on `http://localhost:8080`.
3. **Swagger UI**: Navigate to `http://localhost:8080/docs` to test the endpoints interactively.

### Local Development (Without Docker)

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload --port 8080
   ```

## 🧪 Testing the RBAC

1. Go to the Swagger UI (`/docs`).
2. Use `/api/v1/auth/register` to create a user. By default, they get the `user` role.
3. Login using the "Authorize" button at the top right to get your JWT.
4. Try to access `/api/v1/admin/dashboard`. You will get a `403 Forbidden` error because your role is not `admin`.
5. Try to access `/api/v1/users/me`. You will get a `200 OK` response because it only requires a valid token.

## 📁 Architecture Details

For a detailed breakdown of the design patterns used, see the [Architecture Documentation](docs/ARCHITECTURE.md).

## 👨‍💻 Author

*Created as a technical showcase for enterprise backend engineering.*
