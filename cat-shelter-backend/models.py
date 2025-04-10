from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

favorites = Table(
    'favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('cat_id', Integer, ForeignKey('cats.id'), primary_key=True)
)

class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(String)  # Изменено с Integer на String
    color = Column(String)
    breed = Column(String)
    gender = Column(String)     
    description = Column(String)
    photo_url = Column(String, nullable=True)
    booked_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_sterilized = Column(Boolean, default=False)
    has_rabies_vaccine = Column(Boolean, default=False)

    booked_by = relationship("User", back_populates="booked_cats")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    booked_cats = relationship("Cat", back_populates="booked_by")
    favorite_cats = relationship("Cat", secondary=favorites, backref="favorited_by")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)  # passed/failed
    passed_at = Column(DateTime, default=datetime.utcnow)
    answers = Column(JSON)  # Хранение ответов в формате JSON