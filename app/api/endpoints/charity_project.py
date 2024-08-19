from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB
)
from app.crud.charity_project import charity_project_crud
from app.services.investing import invested_amount_for_projects

charity_project_router = APIRouter()


@charity_project_router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@charity_project_router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await invested_amount_for_projects(session)
    return new_project


@charity_project_router.post(
    '/test',
    response_model=list[CharityProjectDB],
)
async def test(
        session: AsyncSession = Depends(get_async_session)
):
    result = await invested_amount_for_projects(session)
    return result
