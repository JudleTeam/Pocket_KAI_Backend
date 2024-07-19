from pocket_kai.domain.exceptions.base import CoreError


class StudentError(CoreError): ...


class StudentAlreadyExistsError(StudentError): ...


class StudentNotFoundError(StudentError): ...
