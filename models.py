import datetime

from pydantic import BaseModel, Field


class InputUser(BaseModel):
    name: str = Field(title="Name")
    surname: str = Field(title="Surname")
    password: str = Field(title="Password", min_length=6)
    email: str = Field(title="E-mail", min_length=5)


class User(InputUser):
    id: int


class InputGood(BaseModel):
    name: str = Field(title="Name")
    description: str = Field(title="Description")
    price: str = Field(title="Price", min_length=1)


class Good(InputGood):
    id: int


class InputOffer(BaseModel):
    user_id: int
    good_id: int
    status: bool
    cur_time: datetime.datetime


class Offer(InputOffer):
    id: int
