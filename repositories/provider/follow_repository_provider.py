from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import FollowerRelationshipEntity
from repositories.base.follow_repository_base import FollowRepositoryBase


class FollowRepositoryProvider(FollowRepositoryBase):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self,
       follower_id: int | None = None,
       followed_id: int | None = None,
       receive_post: bool | None = None,
       receive_comment: bool | None = None,
    ) -> list[FollowerRelationshipEntity]:

        stmt = select(FollowerRelationshipEntity)

        if follower_id is not None:
            stmt = stmt.where(FollowerRelationshipEntity.follower_id == follower_id)

        if followed_id is not None:
            stmt = stmt.where(FollowerRelationshipEntity.followed_id == followed_id)

        if receive_post is not None:
            stmt = stmt.where(FollowerRelationshipEntity.receive_post == receive_post)

        if receive_comment is not None:
            stmt = stmt.where(FollowerRelationshipEntity.receive_comment == receive_comment)

        stmt = stmt.order_by(FollowerRelationshipEntity.created_at.desc())

        datas = await self.db.execute(stmt)

        return list(datas.scalars().all())