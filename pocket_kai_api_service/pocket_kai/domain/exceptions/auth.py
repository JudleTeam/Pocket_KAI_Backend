from pocket_kai.domain.exceptions.base import CoreError


class NotAuthenticatedError(CoreError):
    pass


class InvalidTokenTypeError(CoreError):
    """Внутренняя ошибка. Выбрасывается при попытке создать токен с неподдерживаемым типом"""


class InvalidTokenPayloadError(CoreError):
    """Внутренняя ошибка. Выбрасывается при попытке создать токен с неподдерживаемым payload"""


class InvalidTokenError(CoreError):
    pass


class BadTokenTypeError(InvalidTokenError):
    pass


class CantRevokeRefreshTokenError(CoreError):
    pass
