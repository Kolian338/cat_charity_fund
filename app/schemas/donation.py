from datetime import datetime

from pydantic import PositiveInt, Field

from app.schemas.base import MyBaseModel


class DonationCommon(MyBaseModel):
    id: int
    create_date: datetime


class DonationBase(MyBaseModel):
    full_amount: PositiveInt
    comment: str | None = Field(None, example='Котикам')

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    pass


class DonationCreateResponse(DonationCommon, DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None
