from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


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
