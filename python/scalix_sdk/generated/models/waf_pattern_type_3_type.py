from enum import Enum


class WafPatternType3Type(str, Enum):
    BODY_SIZE_LIMIT = "body_size_limit"

    def __str__(self) -> str:
        return str(self.value)
