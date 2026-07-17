from enum import Enum


class WafPatternType5Type(str, Enum):
    GEO_BLOCK = "geo_block"

    def __str__(self) -> str:
        return str(self.value)
