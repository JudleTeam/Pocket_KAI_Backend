from pocket_kai.domain.exceptions.base import CoreError


class ExamError(CoreError): ...


class ExamNotFoundError(ExamError): ...
