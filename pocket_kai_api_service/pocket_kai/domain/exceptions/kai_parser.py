from pocket_kai.domain.exceptions.base import CoreError


class KaiParserApiError(CoreError):
    pass


class KaiParsingError(KaiParserApiError):
    pass


class BadKaiCredentialsError(KaiParserApiError):
    pass
