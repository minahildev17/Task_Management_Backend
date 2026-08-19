# Task Management Backend

A backend system for managing users, organizations, projects, tickets, ticket assignments, attachments, and activity-related data.

Built using **FastAPI, SQLAlchemy, MySQL, Alembic, JWT Authentication, MinIO, and Cloudflare Tunnel**.

---

## 🚀 Technologies Used

* Python
* FastAPI
* SQLAlchemy ORM
* MySQL
* Alembic
* Pydantic
* PyMySQL
* JWT Authentication
* Password Hashing
* MinIO
* Python Multipart
* Swagger / OpenAPI
* Cloudflare Tunnel

---

## 📌 Project Features

### Authentication

* User Signup
* User Login
* JWT Authentication
* Password Hashing
* Protected API endpoints

### Organization Management

* Create Organization
* Update Organization
* Delete Organization
* Organization Logo
* Organization Theme
* Assign Users to Organizations

### Project Management

* Create Project
* Update Project
* Delete Project
* Project members support

### Ticket Management

* Create Ticket
* Update Ticket
* Delete Ticket
* Assign Tickets to Users
* Ticket Status Workflow

### Ticket Status Workflow

The ticket status workflow contains the following statuses:

```text
Ready to Do
     ↓
In Progress
     ↓
Testing
     ↓
Done
```

The workflow also supports blocked and return transitions:

```text
Ready to Do → In Progress
Ready to Do → Blocked

In Progress → Ready to Do
In Progress → Blocked
In Progress → Testing

Blocked → In Progress

Testing → Done
Testing → In Progress

Done → In Progress
```

Existing `Pending` task values were migrated to `Ready to Do`.

### File Attachments

* Ticket image/file attachments
* MinIO object storage integration
* `task-attachments` MinIO bucket
* Database stores the file URL/path instead of Base64 image data
* Attachment API support

---

## 🗄️ Database

The project uses **MySQL**.

Example database configuration:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=task_management_db
DB_USER=root
DB_PASSWORD=your_password
```

> Do not upload the actual `.env` file or database password to GitHub.

---

## 📦 MinIO Storage

MinIO is used for storing ticket attachments and images.

### Local MinIO Configuration

```env
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=your_minio_password
MINIO_BUCKET=task-attachments
```

### MinIO Services

```text
MinIO API:
http://127.0.0.1:9000

MinIO Console:
http://127.0.0.1:9001
```

The project uses the following bucket:

```text
task-attachments
```

> The actual MinIO password must only be stored in the local `.env` file and must never be committed to GitHub.

---

## 🔄 Database Migrations

Alembic is used to manage database schema changes.

Run the latest migrations with:

```bash
alembic upgrade head
```

Create a new migration when required:

```bash
alembic revision --autogenerate -m "migration message"
```

---

## 🚀 Run Locally

### 1. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=task_management_db
DB_USER=root
DB_PASSWORD=your_password

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=your_minio_password
MINIO_BUCKET=task-attachments
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start FastAPI server

```bash
uvicorn main:app --reload
```

The local server will be available at:

```text
http://127.0.0.1:8000
```

---

## 📖 Swagger / OpenAPI

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test:

* Authentication APIs
* Organization APIs
* Project APIs
* Ticket APIs
* Ticket assignment
* Attachment upload
* Other available backend endpoints

---

## 🌐 Cloudflare Tunnel

Cloudflare Tunnel can be used to expose the local FastAPI server publicly.

Run:

```bash
cloudflared tunnel --url http://localhost:8000
```

Cloudflare will generate a public `trycloudflare.com` URL.

The public URL can be used to access the FastAPI application and Swagger documentation.

---

## 📂 Main Project Structure

```text
Task Management Backend/
│
├── alembic/
│   └── versions/
│       └── Database migration files
│
├── models/
│   ├── organization.py
│   ├── user.py
│   ├── role.py
│   ├── permissions.py
│   ├── organization_members.py
│   ├── project.py
│   ├── project_members.py
│   ├── task.py
│   ├── comment.py
│   ├── attachment.py
│   └── theme.py
│
├── routers/
│   ├── auth.py
│   ├── organization.py
│   ├── organization_member.py
│   ├── user.py
│   ├── project.py
│   ├── task.py
│   └── attachment.py
│
├── schemas/
│   ├── organization_schema.py
│   ├── project_schema.py
│   ├── task_schema.py
│   └── attachment_schema.py
│
├── services/
│   ├── auth_service.py
│   └── minio_service.py
│
├── utils/
│   ├── security.py
│   └── s3.py
│
├── main.py
├── requirements.txt
├── test_minio.py
├── .env
└── README.md
```

---

## 🔐 Security

Sensitive configuration is stored in `.env`.

The following files and directories should not be committed:

```text
.env
venv/
__pycache__/
*.pyc
.vscode/
.idea/
```

The `.env` file is included in `.gitignore`.

Never commit:

* Database passwords
* MinIO passwords
* JWT secret keys
* Other private credentials

---

## 🧪 Testing

The backend APIs can be tested using Swagger.

Testing includes:

* User Signup
* User Login
* JWT Authentication
* Organization Create / Update / Delete
* User Organization Assignment
* Project Create / Update / Delete
* Ticket Create / Update / Delete
* Ticket Assignment
* Ticket Status Workflow
* Ticket Attachment Upload
* MinIO connectivity
* Database records and migration verification

MinIO connectivity can also be checked using the project's MinIO test script.

---

## 📊 Project Status

### Completed

* Database design
* SQLAlchemy models
* Alembic migrations
* MySQL integration
* FastAPI server
* JWT authentication
* User Signup
* User Login
* Organization CRUD
* Organization Logo support
* Organization Theme support
* Organization Member assignment
* Project CRUD
* Ticket CRUD
* Ticket assignment
* Ticket status workflow
* MinIO configuration
* MinIO bucket setup
* Attachment model and API integration

### In Progress

* Final MinIO image upload debugging
* End-to-end attachment upload verification
* Final API testing
* Final database verification

---

## 👩‍💻 Project

**Task Management Backend**

Backend API developed using FastAPI with MySQL database, SQLAlchemy ORM, Alembic migrations, JWT authentication, and MinIO object storage.
