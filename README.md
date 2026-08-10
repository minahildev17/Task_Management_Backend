# Task Management Backend

A backend system for managing users, organizations, projects, tasks, and related activities.
Built using **FastAPI, SQLAlchemy, MySQL, Alembic, JWT Authentication, and Cloudflare Tunnel**.

## 🚀 Technologies Used

* Python
* FastAPI
* SQLAlchemy
* MySQL
* Alembic
* JWT Authentication
* Pydantic
* PyMySQL
* Cloudflare Tunnel
* Swagger / OpenAPI

## 📌 Project Features

* User Signup
* User Login
* JWT Authentication
* Password Hashing
* Organization Creation
* Organization Update
* Organization Deletion
* Organization Logo
* Organization Theme
* Assign Users to Organizations
* MySQL Database Integration
* Alembic Database Migrations
* Swagger API Documentation
* Cloudflare Tunnel Public Hosting

## 🌐 Live API

**Cloudflare Public URL:**
https://compared-instances-but-inclusive.trycloudflare.com

**Swagger API Documentation:**
https://compared-instances-but-inclusive.trycloudflare.com/docs

## 📚 API Documentation

The project provides interactive Swagger documentation through FastAPI.

Use the Swagger URL above to:

* Register a user
* Login
* Get JWT access token
* Test authenticated endpoints
* Create organizations
* Update organizations
* Delete organizations
* Assign users to organizations

## 🗄️ Database

The project uses **MySQL** with the following database configuration:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=task_management_db
DB_USER=root
DB_PASSWORD=your_password
```

> Do not upload the actual `.env` file or database password to GitHub.

## 🔐 Authentication

Authentication is implemented using **JWT (JSON Web Tokens)**.

Passwords are securely hashed before being stored in the database.

After login, the API returns an access token that can be used to access protected endpoints.

## 🛠️ Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## ☁️ Cloudflare Tunnel

To make the local FastAPI server publicly accessible:

```bash
cloudflared tunnel --url http://localhost:8000
```

Cloudflare generates a public `trycloudflare.com` URL.

## 📂 Main Project Components

* `app/main.py` — FastAPI application
* `app/models/` — SQLAlchemy database models
* `app/schemas/` — Pydantic schemas
* `app/routers/` — API routes
* `app/services/` — Business logic and authentication services
* `app/utils/` — Security utilities
* `alembic/` — Database migrations
* `.env` — Environment variables

## ⚠️ Security

The `.env` file contains sensitive database credentials and must not be committed to GitHub.

Make sure `.env` is included in `.gitignore`.

## 👩‍💻 Project Status

**Completed**

The backend API, database integration, authentication, organization management, Swagger documentation, and Cloudflare public hosting have been implemented.
