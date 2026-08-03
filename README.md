# Task Management Backend

A FastAPI-based backend for a Task Management System. This project uses SQLAlchemy ORM with MySQL for database management and Alembic for database migrations.

## Tech Stack

* Python
* FastAPI
* SQLAlchemy ORM
* MySQL
* Alembic
* Pydantic

## Features

### Implemented

* User signup
* User login
* Organization creation
* Organization update
* Organization deletion
* Organization logo and theme support
* Assign users to organizations
* SQLAlchemy ORM integration
* Alembic database migrations
* Swagger API documentation

### Database Entities

* Users
* Organizations
* Roles
* Organization Members
* Permissions
* Projects
* Project Members
* Tasks
* Comments
* Attachments
* Activity History

## API Endpoints

### Authentication

* `POST /auth/signup`
* `POST /auth/login`

### Organizations

* `POST /organizations`
* `PUT /organizations/{organization_id}`
* `DELETE /organizations/{organization_id}`

### Organization Members

* `POST /organization-members/assign`

## Database

Database: **MySQL**

ORM: **SQLAlchemy**

Migration Tool: **Alembic**

## API Documentation

After running the server, Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project

```bash
cd Task-Management-Backend
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and configure your MySQL database credentials.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=task_management_db
DB_USER=your_username
DB_PASSWORD=your_password
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 7. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```
