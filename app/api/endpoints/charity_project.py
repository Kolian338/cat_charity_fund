from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_name_duplicate, check_project_has_no_investments,
    check_project_is_open, check_required_amount_is_less_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
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


@charity_project_router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    project_db = await check_project_is_open(project_id, session)
    await check_required_amount_is_less_invested(
        obj_in.full_amount, project_db
    )
    project_db = await charity_project_crud.update(
        db_obj=project_db,
        obj_in=obj_in,
        session=session
    )
    await invested_amount_for_projects(session)
    return project_db


@charity_project_router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_has_no_investments(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project
