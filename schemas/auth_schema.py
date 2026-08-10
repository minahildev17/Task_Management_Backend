from pydantic import BaseModel


class SignupRequest(BaseModel):
    Name: str
    Email: str
    Password: str


class LoginRequest(BaseModel):
    Email: str
    Password: str


class SignupResponse(BaseModel):
    message: str
    user_id: int


class LoginResponse(BaseModel):
    message: str
    user_id: int
    access_token: str
    token_type: str