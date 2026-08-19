# Task Management Backend

Backend system for managing users, organizations, projects, tickets, assignments, and attachments.

Built with **FastAPI, SQLAlchemy, MySQL, Alembic, JWT Authentication, and MinIO**.

## Technologies

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Alembic
* JWT Authentication
* MinIO
* Swagger / OpenAPI

## Features

* User Signup & Login
* JWT Authentication
* Organization CRUD
* Organization Logo & Theme
* Organization Member Assignment
* Project CRUD
* Ticket CRUD
* Ticket Assignment
* Ticket Status Workflow
* Ticket Attachments using MinIO
* Database Migrations with Alembic

## Ticket Status Workflow

```text
Ready to Do → In Progress → Testing → Done
                    ↓
                 Blocked
```

Additional valid transitions are implemented according to the ticket workflow.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start the server:

```bash
uvicorn main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## MinIO

MinIO is used for storing ticket attachments and images.

The MinIO configuration is stored in the local `.env` file.

> Do not commit `.env` or any database, MinIO, or JWT credentials to GitHub.

## Project Structure

```text
models/       → Database models
schemas/      → Pydantic schemas
routers/      → API endpoints
services/     → Business logic and MinIO service
utils/        → Security utilities
alembic/      → Database migrations
main.py       → FastAPI application
```

## Status

Core backend functionality is implemented. Final MinIO upload testing and end-to-end verification are in progress.
