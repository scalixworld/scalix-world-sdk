from enum import Enum


class WafPatternType6Type(str, Enum):
    SQL_INJECTION = "sql_injection"

    def __str__(self) -> str:
        return str(self.value)
