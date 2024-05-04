class KaiApiError(Exception):
    """Can't get data from Kai site"""


class ParsingError(Exception):
    """Can't parse data from kai.ru"""


class BadCredentials(Exception):
    """Bad credentials for login"""
