from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.institute import InstituteEntity


class InstituteReader(Protocol):
    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> InstituteEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> InstituteEntity:
        raise NotImplementedError


class InstituteSaver(Protocol):
    @abstractmethod
    async def save(self, institute: InstituteEntity) -> None:
        raise NotImplementedError


class InstituteGatewayProtocol(InstituteReader, InstituteSaver, Protocol): ...
