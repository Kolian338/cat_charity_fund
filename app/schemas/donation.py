from datetime import datetime

from pydantic import BaseModel, PositiveInt, Field


class DonationCommon(BaseModel):
    id: int
    create_date: datetime


class DonationBase(BaseModel):
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
