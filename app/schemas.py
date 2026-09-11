from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .models import Role

class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: Role
    is_active: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class SiteCreate(BaseModel):
    name: str
    region: str
    country: str = 'Ghana'
    category: str
    short_description: str
    story: str
    audio_url: str | None = None
    image_url: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    qr_code: str
    is_published: bool = True

class SiteOut(SiteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1200)
    site_id: int | None = None

class PassportOut(BaseModel):
    points: int
    badges: list[dict]
