from pocket_kai.domain.exceptions.base import CoreError


class LessonError(CoreError): ...


class LessonNotFoundError(LessonError): ...
