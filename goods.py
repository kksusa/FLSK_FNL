from models import *
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import Request
from db import *
from fastapi.templating import Jinja2Templates
import random

templates = Jinja2Templates(directory="templates")
router = APIRouter()
descriptions = ["Классный товар", "Плохой товар", "Прекрасный товар", "Отличный товар"]


# Создание тестовых товаров
@router.get("/fake_goods/{count}")
async def create_note(count: int):
    for i in range(1, count + 1):
        query = goods_db.insert().values(
            name=f'name_{i}',
            description=random.choice(descriptions),
            price=random.randrange(1000))
        await db.execute(query)
    return {'message': f'{count} fake goods created'}


# Создание нового товара
@router.post("/goods/new/", response_model=Good)
async def create_good(good: InputGood):
    query = goods_db.insert().values(
        name=good.name,
        description=good.description,
        price=good.price)
    last_record_id = await db.execute(query)
    return {**good.model_dump(), "id": last_record_id}


# Список товаров
@router.get("/goods/", response_model=list[Good])
async def read_goods():
    query = goods_db.select()
    return await db.fetch_all(query)


# Просмотр одного товара
@router.get("/goods/id/{good_id}", response_model=Good)
async def read_good(good_id: int):
    query = goods_db.select().where(goods_db.c.id == good_id)
    return await db.fetch_one(query)


# Редактирование товара
@router.put("/goods/replace/{good_id}", response_model=Good)
async def update_good(good_id: int, new_good: InputGood):
    query = goods_db.update() \
        .where(goods_db.c.id == good_id) \
        .values(**new_good.model_dump())
    await db.execute(query)
    return {**new_good.model_dump(), "id": good_id}


# Удаление товара
@router.delete("/goods/del/{good_id}")
async def delete_good(good_id: int):
    query = goods_db.delete().where(goods_db.c.id == good_id)
    await db.execute(query)
    return {'message': 'Good deleted'}


# Вывод товаров в HTML
@router.get("/l_goods/", response_class=HTMLResponse)
async def list_goods(request: Request):
    query = goods_db.select()
    return templates.TemplateResponse("db_goods.html",
                                      {"request": request,
                                       'goods': await db.fetch_all(query)})
