from app.crud.base import CRUDBase
from app.models.donation import Donation

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationCreate
)


class CRUDDonations(CRUDBase):
    pass


donations_crud = CRUDDonations(Donation)
