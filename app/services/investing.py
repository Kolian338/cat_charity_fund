from datetime import datetime

from app.core.db import get_async_session
from app.models import CharityProject, Donation
from app.schemas.charity_project import CharityProjectCreate
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.crud.donation import donations_crud
from app.crud.charity_project import charity_project_crud


async def invested_amount_for_projects(
        session: AsyncSession
):
    """
    Процесс инвестирования.

    Запускается после добавления нового проекта или доната.
    Сначала донаты будут распределены по старым проектам(если они открыты).
    Если донат больше чем нужно то оставшаяся часть будет ждать подходяшего проекта.
    """
    # Берем из БД открытые проекты и донаты
    free_donations_db = await donations_crud.get_open_for_investment(session)
    open_projects_db = await charity_project_crud.get_open_for_investment(
        session
    )
    # Сортируем проекты от старых к новым
    open_projects_db = sorted(open_projects_db, key=lambda x: x.create_date)

    for current_project in open_projects_db:
        for current_donation in free_donations_db:
            # Сколько еще нужно донатов проекту
            project_required_amount = (current_project.full_amount
                                       - current_project.invested_amount)
            # свободные деньги из доната
            dontaion_balance = (current_donation.full_amount
                                - current_donation.invested_amount)
            # Если остаточная сумма проекта больше или равна донату
            if project_required_amount >= dontaion_balance:
                # ... то берем весь донат
                current_donate_sum = dontaion_balance
            else:
                # Если остаточная сумма меньше чем донат
                # то берем от доната только требуемую сумму
                current_donate_sum = project_required_amount

            # Добавляем в проект доступную сумму из доната
            current_project.invested_amount += current_donate_sum
            # Учитываем в донате пожертвованную сумму
            current_donation.invested_amount += current_donate_sum

            # Проверяем все ли донатные деньги использованы
            check_fully_invested(current_donation)
            # Проверяем набрал ли проект всю сумму
            if check_fully_invested(current_project):
                # Завершаем обход донатов
                break

    # После всех операций коммитим транзакцию
    await session.commit()

    # Обновляем объекты
    for project in open_projects_db:
        await session.refresh(project)
    for donation in free_donations_db:
        await session.refresh(donation)


def check_fully_invested(obj: CharityProject | Donation):
    """Проверка набрали ли проект нужную сумму или использован весь донат."""
    if obj.invested_amount == obj.full_amount:
        # Если все деньги использованы из доната или проект набрал всю сумму
        # то устанавливаем fully_invested в true
        # и ставим дату закрытия
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return True
    return False
