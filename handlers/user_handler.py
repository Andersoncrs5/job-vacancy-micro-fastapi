import structlog

from schemas.event_message_email import EventMessageEmail
from services.provider.user_service_provider import UserServiceProvider

logger = structlog.get_logger()

class UserHandler:
    def __init__(self, event: EventMessageEmail, service: UserServiceProvider):
        self.event = event
        self.service = service

    async def handle(self):

        user = await self.service.get_by_email(self.event.email)