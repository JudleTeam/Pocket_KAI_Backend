from pocket_kai.domain.exceptions.base import CoreError


class RefreshTokenError(CoreError): ...


class RefreshTokenNotFoundError(RefreshTokenError): ...
