from abc import ABC, abstractmethod

from configs.db.database import UserMetricEntity
from schemas.event_message_schemas import SumRedEnum


class UserMetricServiceBase(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserMetricEntity | None:
        pass

    @abstractmethod
    async def post_count_sum_red(self, metric: UserMetricEntity, action: SumRedEnum) -> UserMetricEntity:
        pass