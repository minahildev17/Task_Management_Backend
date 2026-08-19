from fastapi import FastAPI

from database import engine

from routers import auth
from routers import organization
from routers import organization_member
from routers import user
from routers import project
from routers import task
from routers import attachment


app = FastAPI(
    title="Task Management System",
    description="Backend for Task Management System",
    version="1.0.0"
)


# --------------------------------------------------
# EXISTING ROUTERS
# --------------------------------------------------

app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(organization_member.router)
app.include_router(user.router)


# --------------------------------------------------
# PROJECT / TICKET / ATTACHMENT ROUTERS
# --------------------------------------------------

app.include_router(project.router)
app.include_router(task.router)
app.include_router(attachment.router)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Task Management Backend is running!"
    }