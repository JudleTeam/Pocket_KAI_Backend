from pocket_kai.domain.exceptions.base import CoreError


class GroupError(CoreError): ...


class GroupNotFoundError(GroupError): ...


class GroupAlreadyExistsError(GroupError): ...
