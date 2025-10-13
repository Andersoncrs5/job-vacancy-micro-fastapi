from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import UserEntity
from repositories.base.user_repository_base import UserRepositoryBase


class UserRepositoryProvider(UserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> UserEntity:
        stmt = select(UserEntity).where(
            UserEntity.email == email
        )

        result = await self.db.execute(stmt)

        metric = result.scalars().first()

        if metric is None:
            raise ValueError("UserEntity not found")

        return metric