from pocket_kai.domain.exceptions.base import CoreError


class UserError(CoreError): ...


class UserNotFoundError(UserError): ...
