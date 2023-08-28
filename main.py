import uvicorn

import goods
from db import *
from fastapi import FastAPI
import offers
import users_1

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.include_router(users_1.router, tags=['users'])
app.include_router(goods.router, tags=['goods'])
app.include_router(offers.router, tags=['offers'])

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8005,
        reload=True
    )
