from abc import abstractmethod

from typing import Protocol

from pocket_kai.domain.entitites.speciality import SpecialityEntity


class SpecialityReader(Protocol):
    @abstractmethod
    async def get_by_kai_id(self, kai_id: int) -> SpecialityEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> SpecialityEntity:
        raise NotImplementedError


class SpecialitySaver(Protocol):
    @abstractmethod
    async def save(self, speciality: SpecialityEntity) -> None:
        raise NotImplementedError


class SpecialityGatewayProtocol(SpecialityReader, SpecialitySaver, Protocol): ...
