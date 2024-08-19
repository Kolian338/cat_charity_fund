from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donations_crud
from app.models import User
from app.schemas.donation import (
    DonationDB, DonationCreate, DonationCreateResponse
)
from app.core.user import current_superuser, current_user
from app.services.investing import invested_amount_for_projects

donations_router = APIRouter()


@donations_router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donations_crud.get_multi(session)
    return all_donations


@donations_router.post(
    '/',
    response_model=DonationCreateResponse,
)
async def create_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)

):
    new_donation = await donations_crud.create(
        obj_in=donation, user=user, session=session
    )
    await invested_amount_for_projects(session)
    return new_donation
