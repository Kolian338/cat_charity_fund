from app.crud.base import CRUDBase
from app.models.donation import Donation

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationCreate
)


class CRUDDonations(CRUDBase):

    async def get_donations_by_user_id(
            self,
            user_id: int,
            session: AsyncSession
    ):
        """Получить донаты юзера."""
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id
            )
        )
        return donations.scalars().all()


donations_crud = CRUDDonations(Donation)
