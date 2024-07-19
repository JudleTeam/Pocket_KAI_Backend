from pocket_kai.domain.exceptions.base import CoreError


class DepartmentError(CoreError): ...


class DepartmentNotFoundError(DepartmentError): ...


class DepartmentAlreadyExistsError(DepartmentError): ...
