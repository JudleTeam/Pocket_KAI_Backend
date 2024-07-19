from datetime import datetime

from pocket_kai.application.interfaces.common import DateTimeManager


class UTCDateTimeManager(DateTimeManager):
    def now(self) -> datetime:
        return datetime.utcnow()
