from datetime import datetime

from pydantic import (PositiveInt, Field, NonNegativeInt)

from app.schemas.base import MyBaseModel


class CharityProjectBase(MyBaseModel):
    name: str = Field(
        None,
        min_length=1,
        max_length=100,
        example='Новый проект №1'
    )
    description: str = Field(
        None,
        min_length=1,
        example='На корм котикам'
    )
    full_amount: PositiveInt = Field(
        None,
        example=10_000
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example='Новый проект №1'
    )
    description: str = Field(
        ...,
        min_length=1,
        example='На корм котикам'
    )
    full_amount: PositiveInt = Field(
        ...,
        example=10_000
    )


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    class Config:
        orm_mode = True
