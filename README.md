# TaskFlow API

A production-ready task management REST API built with FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, JWT authentication, Docker, and modern backend best practices.

## 🚀 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT Authentication
- Docker & Docker Compose
- Pytest
- Ruff
- Uvicorn

## ✨ Features

- User Authentication & Authorization
- Project & Task Management
- Comments & Attachments
- Role-Based Access Control (RBAC)
- Pagination, Filtering & Search
- Database Migrations
- Background Tasks
- File Uploads
- API Documentation (Swagger/OpenAPI)
- Production-Ready Project Structure

## 🛠️ Database Migrations (Alembic)

To generate a new database migration:
```bash
alembic revision --autogenerate -m "add user_id to tasks"
```

To apply migrations and upgrade the database schema:
```bash
alembic upgrade head
```

