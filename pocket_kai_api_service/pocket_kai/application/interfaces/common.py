from typing import Protocol


class UUIDGenerator(Protocol):
    def __call__(self) -> str: ...


class DateTimeManager(Protocol):
    def now(self): ...
