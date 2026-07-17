from enum import Enum


class WafPatternType2Type(str, Enum):
    HEADER_MATCH = "header_match"

    def __str__(self) -> str:
        return str(self.value)
