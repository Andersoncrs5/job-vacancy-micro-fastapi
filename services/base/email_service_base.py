from abc import ABC, abstractmethod
from typing import List


class EmailServiceBase(ABC):

    @abstractmethod
    def send_email(
            self,
            to_email: str,
            subject: str,
            html_content: str,
            cc: List[str] = None,
            bcc: List[str] = None,
    ):
        pass