from enum import Enum


class WafPatternType4Type(str, Enum):
    RATE_LIMIT = "rate_limit"

    def __str__(self) -> str:
        return str(self.value)
