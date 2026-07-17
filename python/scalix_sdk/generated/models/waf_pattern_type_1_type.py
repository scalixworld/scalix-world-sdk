from enum import Enum


class WafPatternType1Type(str, Enum):
    PATH_MATCH = "path_match"

    def __str__(self) -> str:
        return str(self.value)
