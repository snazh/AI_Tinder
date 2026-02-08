from typing import Optional, List, Type, Generic

from pydantic import BaseModel
from sqlalchemy import delete, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v0.common.common_types import ColumnValue
from src.api_v0.common.errors import ItemNotFoundError, ItemAlreadyExistsError
from src.database.models.user import UserRole


class BaseService[ModelType, SchemaType]:

    def __init__(self, model: ModelType, schema: SchemaType):
        self.model = model
        self.schema = schema

    def _to_schema(self, instance: ModelType) -> SchemaType:
        return self.schema.model_validate(instance)

    async def create(self, item_data: BaseModel, session: AsyncSession) -> SchemaType:
        new_item = self.model(**item_data.model_dump())
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return self._to_schema(new_item)

    async def get_by_id(self, session: AsyncSession, item_id: int) -> Optional[SchemaType]:
        instance = await session.get(self.model, item_id)
        return self._to_schema(instance) if instance else None

    async def get_one_by(self, session: AsyncSession, field: str, value: ColumnValue) -> Optional[SchemaType]:
        stmt = select(self.model).where(getattr(self.model, field) == value)
        result = await session.execute(stmt)
        item = result.scalar_one_or_none()
        return self._to_schema(item) if item else None

    async def get_all(self, session: AsyncSession) -> List[SchemaType]:

        stmt = select(self.model)
        result = await session.execute(stmt)
        items = result.scalars().all()
        return [self._to_schema(item) for item in items]

    async def get_all_by(self, session: AsyncSession, field: str, value: ColumnValue) -> List[SchemaType]:
        stmt = select(self.model).where(getattr(self.model, field) == value)
        result = await session.execute(stmt)
        items = result.scalars().all()
        return [self._to_schema(item) for item in items]

    async def update(self, item_id: int, item_update_data: BaseModel, session: AsyncSession) -> bool:
        stmt = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(**item_update_data.model_dump)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount == 0:
            raise ItemNotFoundError(item="", attr="id", value=item_id)
        return True

    async def delete(self, session: AsyncSession, item_id: int) -> bool:
        stmt = (
            delete(self.model)
            .where(self.model.id == item_id)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount == 0:
            return False
        return True

    async def get_all_with_options(self, session: AsyncSession, *options) -> List[SchemaType]:
        stmt = select(self.model).options(*options)
        result = await session.execute(stmt)
        items = result.scalars().all()
        return [self._to_schema(item) for item in items]
