from typing import TypeVar, Generic, Type, Any

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: Type[Model]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, obj_id: int) -> Model | None:
        return await self.session.get(self.model, obj_id)

    async def get_first(self, **values: Any) -> Model | None:
        q = select(self.model).filter_by(**values)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list(self, **values: Any) -> list[Model]:
        q = select(self.model).filter_by(**values)
        res = await self.session.execute(q)
        return list(res.scalars().all())

    async def count(self, **values: Any) -> int:
        q = select(func.count()).select_from(self.model).filter_by(**values)
        res = await self.session.execute(q)
        return int(res.scalar_one())

    async def create(self, obj: Model) -> Model:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: int, **values: Any) -> Model | None:
        values = {k: v for k, v in values.items() if v is not None}

        if not values:
            return None

        q = update(self.model).where(self.model.id == obj_id).values(**values)
        await self.session.execute(q)
        await self.session.flush()
        return await self.get_by_id(obj_id)

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get_by_id(obj_id)
        if obj is None:
            return False
        await self.session.delete(obj)
        return True
