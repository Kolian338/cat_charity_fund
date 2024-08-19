from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from pydantic import BaseModel

from app.models import User

# Кастомные типы
ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
            self,
            model: type(ModelType)
    ):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Получить объект по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_open_for_investment(
            self,
            session: AsyncSession,
    ):
        """Возвращает все открытые проекты или донаты."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.fully_invested != True
            )
        )
        db_obj = db_obj.scalars().all()
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Получить все объекты заданного класса"""
        db_objs = await session.execute(
            select(self.model)
        )
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: User = None
    ):
        """Создать новый объект"""
        # Конвертируем объект в словарь.
        obj_in_data = obj_in.dict()
        # Если пользователь был передан...
        if user:
            # ...то дополнить словарь для создания модели.
            obj_in_data['user_id'] = user.id

        # Создаём объект модели.
        # В параметры передаём пары "ключ=значение",
        # для этого распаковываем словарь.
        db_obj = self.model(**obj_in_data)
        # Добавляем созданный объект в сессию.
        # Никакие действия с базой пока ещё не выполняются.
        session.add(db_obj)
        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        await session.commit()
        # Обновляем объект db_obj: считываем данные из БД,
        # чтобы получить его id.
        await session.refresh(db_obj)
        # Возвращаем только что созданный объект класса CreateSchemaType.
        return db_obj

    async def update(
            self,
            # Объект из БД для обновления.
            db_obj: ModelType,
            # Объект из запроса.
            obj_in: UpdateSchemaType,
            session: AsyncSession
    ):
        """Обновить объект."""
        # Представляем объект из БД в виде словаря.
        obj_data = jsonable_encoder(db_obj)
        # Конвертируем объект с данными из запроса в словарь,
        # исключаем неустановленные пользователем поля.
        update_data = obj_in.dict(exclude_unset=True)

        # Перебираем все ключи словаря, сформированного из БД-объекта.
        for field in obj_data:
            # Если конкретное поле есть в словаре с данными из запроса, то...
            if field in update_data:
                # ...устанавливаем объекту БД новое значение атрибута.
                setattr(db_obj, field, update_data[field])
        # Добавляем обновленный объект в сессию.
        session.add(db_obj)
        # Фиксируем изменения.
        await session.commit()
        # Обновляем объект из БД.
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession
    ):
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        # Не обновляем объект через метод refresh(),
        # следовательно он всё ещё содержит информацию об удаляемом объекте.
        return db_obj
