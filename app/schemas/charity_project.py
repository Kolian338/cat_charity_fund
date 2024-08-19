from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field, NonNegativeInt
import random


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example='Новый проект №1'
    )
    description: str = Field(
        ...,
        example='На корм котикам'
    )
    full_amount: PositiveInt = Field(
        ...,
        example=10_000
    )


class CharityProjectUpdate(CharityProjectCreate):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    class Config:
        orm_mode = True
