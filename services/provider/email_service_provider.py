import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import structlog
from dotenv import load_dotenv

from services.base.email_service_base import EmailServiceBase

load_dotenv()

logger = structlog.get_logger()

GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")

class EmailServiceProvider(EmailServiceBase):

    def send_email(
            self,
            to_email: str,
            subject: str,
            html_content: str,
            cc: List[str] = None,
            bcc: List[str] = None,
    ):
        if SMTP_PORT is None:
            raise ValueError("SMTP_PORT is none")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = GMAIL_SENDER_EMAIL
        msg["To"] = to_email

        if cc:
            msg["Cc"] = ", ".join(cc)

        recipients = [to_email] + (cc or []) + (bcc or [])
        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
                server.starttls()

                server.login(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD)

                server.sendmail(GMAIL_SENDER_EMAIL, recipients, msg.as_string())

            logger.info(f"Email GMAIL sent to {to_email}. Subject: {subject}")

        except smtplib.SMTPAuthenticationError:
            logger.error("Gmail SMTP authentication failed. Check your App Password.")
            raise ConnectionError("Gmail authentication failure.")
        except Exception as e:
            logger.error(f"Failed to send email via Gmail SMTP: {e}")
            raise ConnectionError(f"Email sending failed: {e}")