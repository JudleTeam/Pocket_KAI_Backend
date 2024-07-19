from pocket_kai.domain.exceptions.base import CoreError


class TeacherError(CoreError): ...


class TeacherNotFoundError(CoreError): ...


class TeacherAlreadyExistsError(TeacherError): ...
