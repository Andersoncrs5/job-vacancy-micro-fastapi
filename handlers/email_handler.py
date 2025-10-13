import structlog
import os

from dotenv import load_dotenv

from schemas.event_message_email import EventMessageEmail
from services.provider.email_service_provider import EmailServiceProvider
from services.provider.user_service_provider import UserServiceProvider
from templates.template_manager import TemplateManager

logger = structlog.get_logger()

load_dotenv()

NAME_SITE = os.getenv('NAME_SITE')

class UserHandler:
    def __init__(
            self,
            event: EventMessageEmail,
            service: UserServiceProvider,
            email_service: EmailServiceProvider,
            template_manager: TemplateManager
    ):
        self.event = event
        self.service = service
        self.email_service = email_service
        self.template_manager = template_manager

    async def send_email_welcome(self):
        user = await self.service.get_by_email(self.event.email)

        template_context = {
            "user_name": user.name.split()[0],
            "user_email": user.email,
            "welcome_link": NAME_SITE
        }

        template_name_str = self.event.template_name.value

        html_content = self.template_manager.render_html(
            template_name_str,
            template_context
        )

        self.email_service.send_email(
            to_email=user.email,
            subject=self.event.subject,
            html_content=html_content
        )