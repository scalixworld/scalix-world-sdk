from enum import Enum


class WafPatternType0Type(str, Enum):
    IP_BLOCK = "ip_block"

    def __str__(self) -> str:
        return str(self.value)
