from pocket_kai.domain.exceptions.base import CoreError


class ServiceTokenError(CoreError): ...


class ServiceTokenNotFoundError(ServiceTokenError): ...
