from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
import os
from database import engine, get_db
import requests
import uuid
import json
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Cat Shelter API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

# Настройки для JWT и паролей
SECRET_KEY = "22dd287f511b0ec1b05fae7999c053fb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# Функции для работы с паролями и токенов
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def check_interview_status(current_user: models.User, db: Session):
    last_interview = crud.get_last_interview_by_user(db, current_user.id)
    if not last_interview or last_interview.status != "passed":
        if last_interview and last_interview.status == "failed":
            time_since_last = datetime.utcnow() - last_interview.passed_at
            if time_since_last < timedelta(days=1):
                retry_time = last_interview.passed_at + timedelta(days=1)
                raise HTTPException(
                    status_code=403,
                    detail=f"Вы провалили собеседование. Попробуйте снова после {retry_time.isoformat()}"
                )
        raise HTTPException(
            status_code=403,
            detail="Вы не прошли собеседование или оно не было успешно"
        )
    
UPLOAD_DIR = "static/photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаём папку, если её нет

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    if credentials is None:
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("sub")
        if phone_number is None:
            return None  # Возвращаем None вместо исключения
    except JWTError:
        return None  # Возвращаем None вместо исключения
    user = crud.get_user_by_phone(db, phone_number=phone_number)
    if user is None:
        return None
    return user

# Функция для получения Access Token для GigaChat
def get_access_token():
    rq_uid = str(uuid.uuid4())
    authorization_key = "NGU0ZWZlODktYjU5Mi00NzQ5LWE5MmMtNWRjMGRkYWNlYTY3OmRiNTlhNmRjLTE2NTItNDM5OC1hNjJjLThiMmQyYmU5M2Y0Yg=="
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {authorization_key}'
    }
    payload = {'scope': 'GIGACHAT_API_PERS'}
    try:
        response = requests.post(
            "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            headers=headers,
            data=payload,
            verify=False
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Ошибка получения токена: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {str(e)}")
        return None

ACCESS_TOKEN = get_access_token()
if not ACCESS_TOKEN:
    print("Не удалось получить Access Token при запуске.")

def refresh_access_token():
    global ACCESS_TOKEN
    new_token = get_access_token()
    if new_token:
        ACCESS_TOKEN = new_token
    return ACCESS_TOKEN

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_phone(db, user.phone_number)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login")
def login(data: schemas.LoginRequest = Body(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, data.username)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    # Возвращаем токен и данные пользователя
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number
    }

@app.put("/profile", response_model=schemas.User)
def update_profile(
    user_update: schemas.UserUpdate = Body(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(db, current_user.id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
# Эндпоинт для пользователя: снятие своего бронирования

@app.post("/cats/{cat_id}/unbook", response_model=dict)
def unbook_cat(
    cat_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = crud.unbook_cat(db, cat_id, current_user.id)
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Кот не найден или не забронирован вами"
        )
    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Кот не забронирован, снимать бронирование не требуется"
        )
    return {"message": "Бронирование успешно снято"}

@app.post("/admin/search-booked-cats", response_model=List[schemas.BookedCat])
def search_booked_cats(
    search: schemas.CatSearchQuery = Body(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Только администраторы могут искать забронированных котов"
        )
    booked_cats = crud.search_booked_cats_by_name(db, search.name)
    if not booked_cats:
        return []  # Если ничего не найдено, возвращаем пустой список
    return [
        schemas.BookedCat(cat=cat, user=cat.booked_by)
        for cat in booked_cats
    ]

# Эндпоинт для администратора: снятие любого бронирования
@app.post("/admin/cats/{cat_id}/unbook", response_model=dict)
def admin_unbook_cat(
    cat_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Только администраторы могут снимать любые бронирования"
        )
    result = crud.unbook_cat(db, cat_id)  # Без user_id для админа
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Кот не найден"
        )
    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Кот не забронирован, снимать бронирование не требуется"
        )
    return {"message": "Бронирование успешно снято администратором"}

@app.post("/interview")
async def take_interview(
    interview: schemas.InterviewCreate = Body(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not crud.can_take_interview(db, current_user.id):
        raise HTTPException(status_code=403, detail="Вы не можете пройти собеседование сейчас")
    questions = [
        "Почему вы решили завести кошку?",
        "Были ли у вас животные раньше? Если да, что с ними стало?",
        "Почему вы выбрали именно этого кота/кошку?",
        "Где вы живете?",
        "Каким кормом вы планируете кормить питомца?",
        "Опишите вашу реакцию, когда кошка испортит обои или мебель:",
        "Осознаёте ли, что если животное окажется в плохих условиях, приют оставляет за собой право его изъять? (1 - Да, 2 - Приют не имеет права, 3 - Нет)",
        "Готовы ли вы к возможным болезням кошки, лечению и уходу за ней в старости?",
        "Как будете справляться с кошачьей шерстью и когтеточением?",
        "Вы готовы заключить договор с приютом об ответственном содержании животного? Да или нет."
    ]
    answers_text = ""
    for i, q in enumerate(questions, 1):
        key = f"question_{i}"
        # Валидация Pydantic уже гарантирует наличие всех ключей и непустые значения
        answers_text += f"{q} {interview.answers[key]}\n"
    system_prompt = (
        "Ты — сотрудник приюта для кошек. Я предоставлю тебе ответы пользователя на вопросы собеседования. "
        "Твоя задача — оценить, можно ли пользователю забрать кота из приюта. Суди очень жестко, котик долен попасть в хорошие руки. "
        "Верни только 'да' или 'нет' в зависимости от того, подходят ли ответы для ответственного усыновления."
    )
    user_prompt = f"Ответы пользователя:\n{answers_text}"
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        refresh_access_token()
        if not ACCESS_TOKEN:
            raise HTTPException(status_code=503, detail="Не удалось подключиться к GigaChat")
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 401:
            refresh_access_token()
            headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
            response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            result = response.json()
            gigachat_response = result['choices'][0]['message']['content'].strip().lower()
            status = "passed" if gigachat_response == "да" else "failed"
            crud.create_interview(db, current_user.id, interview.answers, status)
            return {"status": status}
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка GigaChat: {response.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к GigaChat: {str(e)}")

@app.get("/interview/status")
def get_interview_status(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Current user ID: {current_user.id}")  # Отладка
    last_interview = crud.get_last_interview_by_user(db, current_user.id)
    print(f"Last interview: {last_interview}")  # Отладка
    if last_interview:
        return {"status": last_interview.status, "passed_at": last_interview.passed_at}
    else:
        return {"status": "None"}

@app.get("/cats/", response_model=List[schemas.CatWithFavorite])
def read_cats(
    skip: int = 0,
    limit: int = 10,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cats = crud.get_cats(db, skip=skip, limit=limit)
    if current_user:
        favorite_cat_ids = [cat.id for cat in crud.get_favorite_cats(db, current_user.id)]
    else:
        favorite_cat_ids = []
    return [
        schemas.CatWithFavorite(
            **cat.__dict__,
            is_favorite=(cat.id in favorite_cat_ids)
        ) for cat in cats
    ]

@app.get("/cats/{cat_id}", response_model=schemas.CatWithFavorite)
def read_cat(
    cat_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cat = crud.get_cat(db, cat_id=cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    if cat.booked_by_user_id is not None:
        raise HTTPException(status_code=403, detail="Этот кот уже забронирован")
    is_favorite = False
    if current_user:
        is_favorite = cat.id in [fav.id for fav in crud.get_favorite_cats(db, current_user.id)]
    return schemas.CatWithFavorite(
        **cat.__dict__,
        is_favorite=is_favorite
    )
@app.get("/admin/cats/", response_model=List[schemas.CatWithFavorite])
def read_all_cats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администраторы могут просматривать всех котов")
    cats = db.query(models.Cat).all()
    # Для администратора is_favorite всегда False (или можно добавить логику, если нужно)
    return [
        schemas.CatWithFavorite(
            **cat.__dict__,
            is_favorite=False
        ) for cat in cats
    ]

@app.post("/cats/", response_model=schemas.Cat)
def create_cat(cat: schemas.CatCreate = Body(...), db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)

@app.post("/search_cats", response_model=List[schemas.CatWithFavorite])
async def search_cats(
    search: schemas.SearchQuery,
    current_user: models.User = Depends(get_current_user),  # Добавляем текущего пользователя
    db: Session = Depends(get_db)
):
    available_cats = crud.get_available_cats(db)
    if not available_cats:
        return []

    cats_text = "Доступные коты:\n"
    for cat in available_cats:
        cats_text += (
            f"ID: {cat.id}, Имя: {cat.name}, Возраст: {cat.age}, Цвет: {cat.color}, "
            f"Порода: {cat.breed}, Пол: {cat.gender}, Описание: {cat.description}\n"
        )

    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        refresh_access_token()
        if not ACCESS_TOKEN:
            raise HTTPException(status_code=503, detail="Не удалось подключиться к GigaChat")

    system_prompt = (
        "Ты — помощник в приюте для кошек. Я дам тебе список котов и запрос пользователя. "
        "Выбери котов, которые соответствуют запросу, и верни ТОЛЬКО их ID в формате JSON: {\"cat_ids\": [id1, id2, ...]}. "
        "Не возвращай имена или другие данные, только ID в указанном формате. "
        "Если ни один кот не подходит, верни {\"cat_ids\": []}. "
        "Учитывай возраст, цвет, породу, пол и описание при выборе."
    )
    user_prompt = f"Список котов:\n{cats_text}\n\nЗапрос пользователя: {search.query}"

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 401:
            refresh_access_token()
            headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
            response = requests.post(url, headers=headers, json=payload, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            gigachat_response = result['choices'][0]['message']['content']
            try:
                response_data = json.loads(gigachat_response)
                cat_ids = response_data["cat_ids"]
            except json.JSONDecodeError:
                cleaned_response = gigachat_response.strip().replace('"', '').replace('[', '').replace(']', '')
                cat_names = [name.strip() for name in cleaned_response.split(',') if name.strip()]
                cat_ids = [cat.id for cat in available_cats if cat.name in cat_names]

            matched_cats = [cat for cat in available_cats if cat.id in cat_ids]
            # Добавляем is_favorite для каждого кота
            favorite_cat_ids = [cat.id for cat in crud.get_favorite_cats(db, current_user.id)]
            return [
                schemas.CatWithFavorite(
                    **cat.__dict__,
                    is_favorite=(cat.id in favorite_cat_ids)
                ) for cat in matched_cats
            ]
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка GigaChat: {response.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к GigaChat: {str(e)}")
    
@app.put("/cats/{cat_id}", response_model=schemas.Cat)
def update_cat(cat_id: int, cat: schemas.CatCreate = Body(...), db: Session = Depends(get_db)):
    updated_cat = crud.update_cat(db=db, cat_id=cat_id, cat=cat)
    if updated_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return updated_cat

@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    deleted_cat = crud.delete_cat(db=db, cat_id=cat_id)
    if deleted_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return {"message": "Cat deleted successfully"}

@app.post("/cats/{cat_id}/book", response_model=dict)
def book_cat_endpoint(
    cat_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_interview_status(current_user, db)  # Проверка статуса собеседования
    booked_cat = crud.book_cat  (db, cat_id, current_user.id)
    if booked_cat is None:
        raise HTTPException(status_code=400, detail="Кот уже забронирован или не существует")
    return {"message": "Кот успешно забронирован"}

# Добавление/удаление кота в избранное
@app.post("/cats/{cat_id}/favorite", response_model=dict)
def toggle_favorite(
    cat_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем, есть ли кот в избранном
    user_favorites = crud.get_favorite_cats(db, current_user.id)
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Кот не найден")
    
    if cat in user_favorites:
        crud.remove_from_favorites(db, current_user.id, cat_id)
        return {"message": "Кот удалён из избранного"}
    else:
        crud.add_to_favorites(db, current_user.id, cat_id)
        return {"message": "Кот добавлен в избранное"}

# Просмотр списка избранных котов
@app.get("/favorites", response_model=List[schemas.CatWithFavorite])
def get_favorites(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем, что пользователь авторизован
    if not current_user:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    # Получаем только нез забронированных избранных котов
    favorite_cats = crud.get_favorite_cats(db, current_user.id)[skip:skip + limit]
    return [
        schemas.CatWithFavorite(
            **cat.__dict__,
            is_favorite=True  # Все коты в этом запросе в избранном
        ) for cat in favorite_cats
    ]

# Эндпоинт для администраторов: список забронированных котов
@app.get("/admin/booked-cats", response_model=List[schemas.BookedCat])
def get_booked_cats_endpoint(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только администраторы могут просматривать забронированных котов")
    booked_cats = crud.get_booked_cats(db)
    return [
        schemas.BookedCat(cat=cat, user=cat.booked_by)
        for cat in booked_cats
    ]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cat Shelter API",
        version="1.0.0",
        description="API для приюта кошек с авторизацией через JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Список защищённых эндпоинтов
    protected_paths = [
        "/profile",
        "/interview",
        "/interview/status",
        "/cats/{cat_id}/unbook",
        "/cats/{cat_id}/book",
        "/admin/booked-cats",
        "/admin/cats/",
        "/admin/search-booked-cats",
        "/admin/cats/{cat_id}/unbook",
        "/cats/{cat_id}/favorite",  # Новый путь
        "/favorites"
    ]
    # Применяем схему безопасности к защищённым путям
    for path in protected_paths:
        if path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    # Дополнительная настройка описания для /interview (оставляем как есть)
    openapi_schema["paths"]["/interview"]["post"]["requestBody"]["content"]["application/json"]["schema"]["description"] = (
        "Ответы на 10 вопросов:\n"
        "1. Почему вы решили завести кошку?\n"
        "2. Были ли у вас животные раньше? Если да, что с ними стало?\n"
        "3. Почему вы выбрали именно этого кота/кошку?\n"
        "4. Где вы живете?\n"
        "5. Каким кормом вы планируете кормить питомца?\n"
        "6. Опишите вашу реакцию, когда кошка испортит обои или мебель\n"
        "7. Осознаёте ли вы, что приют может изъять животное? (1 - Да, 2 - Нет права, 3 - Нет)\n"
        "8. Готовы ли вы к болезням кошки и уходу?\n"
        "9. Как будете справляться с шерстью и когтеточением?\n"
        "10. Готовы ли вы заключить договор с приютом?"
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi