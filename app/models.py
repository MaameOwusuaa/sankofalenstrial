from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, Float, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import enum

class Role(str, enum.Enum):
    user = 'user'
    admin = 'admin'
    superuser = 'superuser'

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    passport: Mapped['Passport'] = relationship(back_populates='user', uselist=False, cascade='all, delete-orphan')

class HeritageSite(Base):
    __tablename__ = 'heritage_sites'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    region: Mapped[str] = mapped_column(String(120), index=True)
    country: Mapped[str] = mapped_column(String(120), default='Ghana')
    category: Mapped[str] = mapped_column(String(100), index=True)
    short_description: Mapped[str] = mapped_column(String(500))
    story: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    qr_code: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Passport(Base):
    __tablename__ = 'passports'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    points: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship(back_populates='passport')

class Badge(Base):
    __tablename__ = 'badges'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(400))
    awarded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Scan(Base):
    __tablename__ = 'scans'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    site_id: Mapped[int] = mapped_column(ForeignKey('heritage_sites.id'), index=True)
    scanned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    action: Mapped[str] = mapped_column(String(160))
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
