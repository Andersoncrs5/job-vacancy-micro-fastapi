from datetime import datetime
from uuid import UUID

from configs.db.enums import NotificationTypeEnum
from configs.orjson.orjson_config import ORJSONModel

class EventNotification(ORJSONModel):
    event_id: UUID
    event_type: NotificationTypeEnum
    actor_id: int | None
    entity_id: int | None
    created_at: datetime
    source_service: str
    data: dict
    metadata: dict