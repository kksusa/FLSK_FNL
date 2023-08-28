from models import *
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import Request
from db import *
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# Создание тестовых пользователей
@router.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(1, count + 1):
        query = users_db.insert().values(
            name=f'name_{i}',
            surname=f'surname_{i}',
            password=f'pswd_{i}',
            email=f'mail_{i}@mail.ru')
        await db.execute(query)
    return {'message': f'{count} fake users created'}


# Создание нового пользователя
@router.post("/users/new/", response_model=User)
async def create_user(user: InputUser):
    query = users_db.insert().values(
        login=user.login,
        password=user.password,
        email=user.email)
    last_record_id = await db.execute(query)
    return {**user.model_dump(), "id": last_record_id}


# Список пользователей
@router.get("/users/", response_model=list[User])
async def read_users():
    query = users_db.select()
    return await db.fetch_all(query)


# Просмотр одного пользователя
@router.get("/users/id/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users_db.select().where(users_db.c.id == user_id)
    return await db.fetch_one(query)


# Редактирование пользователя
@router.put("/users/replace/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: InputUser):
    query = users_db.update() \
        .where(users_db.c.id == user_id) \
        .values(**new_user.model_dump())
    await db.execute(query)
    return {**new_user.model_dump(), "id": user_id}


# Удаление пользователя
@router.delete("/users/del/{user_id}")
async def delete_user(user_id: int):
    query = users_db.delete().where(users_db.c.id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}


# Вывод пользователей в HTML
@router.get("/l_users/", response_class=HTMLResponse)
async def list_users(request: Request):
    query = users_db.select()
    return templates.TemplateResponse("db_users.html",
                                      {"request": request,
                                       'users': await db.fetch_all(query)})
