import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db.database import NotificationEntity, NotificationEnterpriseEntity
from repositories.base.notification_enterprise_repository_base import NotificationEnterpriseRepositoryBase
from repositories.generics.generic_repository import GenericRepository

logger = structlog.get_logger()

class NotificationEnterpriseRepositoryProvider(
    NotificationEnterpriseRepositoryBase,
    GenericRepository[
        NotificationEnterpriseEntity,
        None,
        int,
        NotificationEnterpriseEntity
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, entity_class=NotificationEnterpriseEntity)