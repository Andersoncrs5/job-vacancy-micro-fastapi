from datetime import datetime
from enum import Enum
from uuid import UUID

from configs.orjson.orjson_config import ORJSONModel


class TemplateEnum(str, Enum):
    welcome_email = 'welcome_email'
    order_confirmation = 'order_confirmation'
    email_bye = 'email_bye'

class EventMessageEmail(ORJSONModel):
    event_id: UUID
    email: str
    template_name: TemplateEnum
    created_at: datetime
    source_service: str
    subject: str
    cc: list[str] | None = None,
    bcc: list[str] | None = None
    data: dict
    metadata: dict