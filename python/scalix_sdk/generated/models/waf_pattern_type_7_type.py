from enum import Enum


class WafPatternType7Type(str, Enum):
    XSS = "xss"

    def __str__(self) -> str:
        return str(self.value)
