from sqlalchemy.orm import Session
from models import Cat
from schemas import CatCreate
from passlib.context import CryptContext
from datetime import datetime, timedelta
import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def can_take_interview(db: Session, user_id: int):
    last_interview = db.query(models.Interview).filter(models.Interview.user_id == user_id).order_by(models.Interview.passed_at.desc()).first()
    if not last_interview or last_interview.status == "passed":
        return True
    if last_interview.passed_at + timedelta(days=180) < datetime.utcnow():
        return True
    return False

def create_interview(db: Session, user_id: int, answers: dict, status: str):
    db_interview = models.Interview(
        user_id=user_id,
        status=status,
        answers=answers
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_last_interview_by_user(db: Session, user_id: int):
    return db.query(models.Interview).filter(models.Interview.user_id == user_id).order_by(models.Interview.passed_at.desc()).first()

def get_cats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cat).filter(models.Cat.booked_by_user_id == None).offset(skip).limit(limit).all()

def get_cat(db: Session, cat_id: int):
    return db.query(Cat).filter(Cat.id == cat_id).first()

def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def unbook_cat(db: Session, cat_id: int, user_id: int = None):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if cat is None:
        return None  # Кот не найден
    # Если передан user_id, проверяем, что кот забронирован этим пользователем
    if user_id is not None and cat.booked_by_user_id != user_id:
        return None  # Кот не забронирован этим пользователем
    # Проверяем, забронирован ли кот вообще
    if cat.booked_by_user_id is None:
        return False  # Кот не забронирован
    # Снимаем бронирование
    cat.booked_by_user_id = None
    db.commit()
    db.refresh(cat)
    return cat  # Успешное снятие брони

def add_to_favorites(db: Session, user_id: int, cat_id: int):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        return None
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    # Проверяем, не добавлен ли кот уже в избранное
    if cat not in user.favorite_cats:
        user.favorite_cats.append(cat)
        db.commit()
    return cat

def remove_from_favorites(db: Session, user_id: int, cat_id: int):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        return None
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    # Проверяем, есть ли кот в избранном
    if cat in user.favorite_cats:
        user.favorite_cats.remove(cat)
        db.commit()
    return cat

def get_favorite_cats(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return []
    # Фильтруем котов, у которых booked_by_user_id IS NULL
    return [cat for cat in user.favorite_cats if cat.booked_by_user_id is None]

def search_booked_cats_by_name(db: Session, name: str):
    # Ищем котов, у которых есть бронирование и имя частично совпадает
    return db.query(models.Cat).filter(
        models.Cat.booked_by_user_id != None,
        models.Cat.name.ilike(f"%{name}%")  # Нечувствительный к регистру поиск по части имени
    ).all()

def update_cat(db: Session, cat_id: int, cat: CatCreate):
    db_cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if db_cat:
        for key, value in cat.dict().items():
            setattr(db_cat, key, value)
        db.commit()
        db.refresh(db_cat)
    return db_cat

def delete_cat(db: Session, cat_id: int):
    db_cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if db_cat:
        db.delete(db_cat)
        db.commit()
    return db_cat

def book_cat(db: Session, cat_id: int, user_id: int):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if cat is None or cat.booked_by_user_id is not None:
        return None  # Кот не существует или уже забронирован
    cat.booked_by_user_id = user_id
    db.commit()
    db.refresh(cat)
    return cat

def get_booked_cats(db: Session):
    return db.query(models.Cat).filter(models.Cat.booked_by_user_id != None).all()

def get_available_cats(db: Session):
    return db.query(models.Cat).filter(models.Cat.booked_by_user_id == None).all()