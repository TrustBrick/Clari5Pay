# schemas.py
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_no: str          # sent by the frontend as a string
    # NOTE: created_at is set by the database (server_default=now()),
    # so the client does NOT send it.


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_name: str


class MessageResponse(BaseModel):
    message: str
    user_id: int


class DashboardResponse(BaseModel):
    message: str
    user_id: str
    email: str
