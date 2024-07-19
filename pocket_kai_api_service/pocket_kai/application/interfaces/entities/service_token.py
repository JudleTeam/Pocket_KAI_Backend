from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.service_token import ServiceTokenEntity


class ServiceTokenReader(Protocol):
    @abstractmethod
    async def get_by_token(self, token: str) -> ServiceTokenEntity:
        """
        :param token:
        :return:
        :raise ServiceTokenNotFoundError:
        """
        raise NotImplementedError
