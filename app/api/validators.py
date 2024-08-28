from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, CharityProjectCreate, \
    CharityProjectUpdate


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    """Проверяет на дубликат имени проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )
    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_name_duplicate_before_update(
        obj_in: CharityProjectUpdate,
        project_db: CharityProjectDB,
        session: AsyncSession,
) -> None:
    if obj_in.name != project_db.name:
        await check_project_name_duplicate(obj_in.name, session)


async def has_project(
        project_id: int,
        session: AsyncSession,
) -> CharityProjectDB:
    """Проверка наличия проекта."""
    project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект отсутствует!'
        )
    return project


async def check_project_is_open(
        project_id: int,
        session: AsyncSession,
) -> CharityProjectDB:
    """Проверка открыт ли проект."""
    project = await has_project(project_id, session)
    if project.close_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


async def check_required_amount_is_less_invested(
        new_amount: int,
        project: CharityProjectDB,
) -> None:
    """Требуемая сумма меньше уже вложенной."""
    if new_amount:
        if new_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    'Нельзя установить требуемую сумму меньше уже вложенной.'
                )
            )


async def check_project_has_no_investments(
        project_id: int,
        session: AsyncSession,
) -> CharityProjectDB:
    """Проверяет были ли инвестиции в проект."""
    project = await has_project(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project
