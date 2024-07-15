from core.exceptions.base import CoreError


class ExternalApiError(CoreError):
    pass


class PocketKaiApiError(ExternalApiError):
    pass


class KaiApiError(ExternalApiError):
    pass
