from abc import ABC, abstractmethod


class EnterpriseFollowUserRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self,
                      enterprise_id: int | None,
                      user_id: int | None,
                      receive_post: bool | None,
                      receive_comment: bool | None,
                      receive_vacancy: bool | None,
                      ):
        pass