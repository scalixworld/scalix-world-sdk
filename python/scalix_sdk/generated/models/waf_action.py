from enum import Enum


class WafAction(str, Enum):
    BLOCK = "block"
    CHALLENGE = "challenge"
    LOG = "log"
    RATE_LIMIT = "rate_limit"

    def __str__(self) -> str:
        return str(self.value)
