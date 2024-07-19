from pocket_kai.domain.exceptions.base import CoreError


class DisciplineError(CoreError): ...


class DisciplineNotFoundError(DisciplineError): ...


class DisciplineAlreadyExistsError(DisciplineError): ...
