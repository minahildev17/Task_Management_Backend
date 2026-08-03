from pydantic import BaseModel


class SignupRequest(BaseModel):
    Name: str
    Email: str
    Password: str


class LoginRequest(BaseModel):
    Email: str
    Password: str


class AuthResponse(BaseModel):
    message: str
    user_id: int