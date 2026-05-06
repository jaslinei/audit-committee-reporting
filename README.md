# Tool-27 — Audit Committee Reporting

AI-powered web application for managing and reporting audit committee findings.

## Architecture
## Prerequisites

- Java 17+
- Maven 3.9+
- Docker Desktop
- Node.js 18+
- Git

## Setup Steps

### 1. Clone the repository
### 2. Create .env file
Fill in all values in the .env file.

### 3. Start all services
### 4. Access the application
- Frontend: http://localhost
- Backend API: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui.html
- AI Service: http://localhost:5000/health

## .env Variables

| Variable | Description | Example |
|----------|-------------|---------|
| DB_URL | PostgreSQL connection URL | jdbc:postgresql://localhost:5432/tool27db |
| DB_USERNAME | Database username | postgres |
| DB_PASSWORD | Database password | yourpassword |
| REDIS_HOST | Redis host | localhost |
| REDIS_PORT | Redis port | 6379 |
| JWT_SECRET | JWT signing secret | your-long-secret-key |
| JWT_EXPIRY | JWT expiry in ms | 86400000 |
| MAIL_HOST | SMTP host | smtp.gmail.com |
| MAIL_PORT | SMTP port | 587 |
| MAIL_USERNAME | Email address | you@gmail.com |
| MAIL_PASSWORD | Email app password | yourapppassword |
| GROQ_API_KEY | Groq AI API key | gsk_xxxxxxxxxxxx |

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Java 17, Spring Boot 3.x |
| Security | Spring Security, JWT |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Migrations | Flyway |
| AI Service | Python, Flask, Groq LLaMA-3.3-70b |
| Vector DB | ChromaDB |
| Frontend | React 18, Vite, Tailwind CSS |
| Container | Docker, Docker Compose |

## Team

| Role | Responsibility |
|------|---------------|
| Java Developer 1 | Spring Boot, JWT, Redis, Email, Tests |
| Java Developer 2 | DB Schema, Repository, Audit Log, Docker |
| Java Developer 3 | React Frontend, Dashboard, Analytics |
| AI Developer 1 | Flask setup, /describe, /recommend, RAG |
| AI Developer 2 | Groq Client, /generate-report, Caching |
| AI Developer 3 | Security, Rate Limiting, OWASP ZAP |
| Security Reviewer | Security testing, SECURITY.md |

## Running Tests
## Demo Day
Friday 9 May 2026 — 8 minute live presentation