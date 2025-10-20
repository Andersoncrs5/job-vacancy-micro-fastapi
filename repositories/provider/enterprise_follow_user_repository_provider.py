from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import EnterpriseFollowsUserEntity
from repositories.base.enterprise_follow_user_repository_base import EnterpriseFollowUserRepositoryBase


class EnterpriseFollowUserRepositoryProvider(EnterpriseFollowUserRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self,
                      enterprise_id: int | None,
                      user_id: int | None,
                      receive_post: bool | None,
                      receive_comment: bool | None,
                      receive_vacancy: bool | None,
                      ):
        stmt = select(EnterpriseFollowsUserEntity)

        if enterprise_id is not None:
            stmt = stmt.where(EnterpriseFollowsUserEntity.enterprise_id == enterprise_id)

        if user_id is not None:
            stmt = stmt.where(EnterpriseFollowsUserEntity.user_id == user_id)

        if receive_post is not None:
            stmt = stmt.where(EnterpriseFollowsUserEntity.receive_post == receive_post)

        if receive_comment is not None:
            stmt = stmt.where(EnterpriseFollowsUserEntity.receive_comment == receive_comment)

        if receive_vacancy is not None:
            stmt = stmt.where(EnterpriseFollowsUserEntity.receive_vacancy == receive_vacancy)

        datas = await self.db.execute(stmt)

        return list(datas.scalars().all())