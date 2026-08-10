from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from database import engine

from routers import auth
from routers import organization
from routers import organization_member
from routers import user


app = FastAPI(
    title="Task Management System",
    description="Backend for Task Management System",
    version="1.0.0"
)


# Create uploads folder automatically
os.makedirs("uploads", exist_ok=True)


# Serve uploaded files
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# Include routers
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(organization_member.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {
        "message": "Task Management Backend is running!"
    }