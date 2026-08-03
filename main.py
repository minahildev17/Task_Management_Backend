from fastapi import FastAPI
from database import engine

from routers import auth
from routers import organization
from routers import organization_member

app = FastAPI(
    title="Task Management System",
    description="Backend for Task Management System",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(organization_member.router)


@app.get("/")
def home():
    return {
        "message": "Task Management Backend is running!",
        "database": str(engine.url)
    }