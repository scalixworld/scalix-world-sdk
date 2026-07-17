from enum import Enum


class ShieldAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    RATE_LIMIT = "rate_limit"

    def __str__(self) -> str:
        return str(self.value)
