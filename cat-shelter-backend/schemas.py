from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CatBase(BaseModel):
    name: str
    age: str
    color: str
    breed: str
    gender: str
    description: str
    photo_url: Optional[str] = None
    is_sterilized: bool = False  # Новое поле: стерилизация
    has_rabies_vaccine: bool = False  # Новое поле: прививка от бешенства

class CatCreate(CatBase):
    pass

class CatWithFavorite(CatBase):
    id: int
    booked_by_user_id: Optional[int] = None
    is_favorite: bool = False  # Новое поле: находится ли кот в избранном

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str

class CatSearchQuery(BaseModel):
    name: str

class Cat(CatBase):
    id: int
    booked_by_user_id: Optional[int] = None  # ID пользователя, забронировавшего кота

    class Config:
        from_attributes = True  
class InterviewCreate(BaseModel):
    answers: dict  # Ответы на 10 вопросов в формате словаря

    class Config:
        # Добавляем пример структуры данных для Swagger
        schema_extra = {
            "example": {
                "answers": {
                    "question_1": "Я хочу завести кошку, чтобы она стала моим другом.",
                    "question_2": "Да, у меня была собака, она умерла от старости.",
                    "question_3": "Этот кот выглядит милым и подходит моему образу жизни.",
                    "question_4": "Я живу в квартире в центре города.",
                    "question_5": "Я планирую кормить премиум-кормом, например, Royal Canin.",
                    "question_6": "Я постараюсь не злиться и куплю когтеточку.",
                    "question_7": "Да",
                    "question_8": "Да, я готов лечить кошку и ухаживать за ней.",
                    "question_9": "Буду регулярно пылесосить и чесать кошку.",
                    "question_10": "Да"
                }
            }
        }
class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class Interview(BaseModel):
    id: int
    user_id: int
    status: str
    passed_at: datetime
    answers: dict
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class BookedCat(BaseModel):
    cat: Cat
    user: User

    class Config:
        from_attributes = True

class FavoriteCat(BaseModel):
    cat: Cat

    class Config:
        from_attributes = True