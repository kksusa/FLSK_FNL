from models import *
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from db import *
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# Список заказов
@router.get("/offers/", response_model=list[Offer])
async def read_offers():
    query = offers_db.select()
    return await db.fetch_all(query)


# Просмотр одного заказа
@router.get("/offers/id/{offer_id}", response_model=Offer)
async def read_offer(offer_id: int):
    query = offers_db.select().where(offers_db.c.id == offer_id)
    return await db.fetch_one(query)


# Создание нового заказа
@router.post('/offers/', response_model=dict)
async def inp_offer(offer: InputOffer):
    query = offers_db.insert().values(
        user_id=offer.user_id,
        good_id=offer.good_id,
        cur_time=offer.cur_time,
        status=offer.status)
    last_record_id = await db.execute(query)
    return {**offer.model_dump(), "id": last_record_id}


# Редактирование заказа
@router.put("/offers/replace/{offer_id}", response_model=Offer)
async def update_offer(offer_id: int, new_offer: InputOffer):
    query = offers_db.update() \
        .where(offers_db.c.id == offer_id) \
        .values(**new_offer.model_dump())
    await db.execute(query)
    return {**new_offer.model_dump(), "id": offer_id}


# Удаление заказа
@router.delete("/offers/del/{offer_id}")
async def delete_offer(offer_id: int):
    query = offers_db.delete().where(offers_db.c.id == offer_id)
    await db.execute(query)
    return {'message': 'Offer deleted'}


# Вывод заказов в HTML
@router.get("/l_offers/", response_class=HTMLResponse)
async def list_offers(request: Request):
    query = offers_db.select()
    return templates.TemplateResponse("db_offers.html",
                                      {"request": request,
                                       'offers': await db.fetch_all(query)})
