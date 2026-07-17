from enum import Enum


class GdprRequestType(str, Enum):
    ACCESS = "access"
    ERASURE = "erasure"
    EXPORT = "export"
    RECTIFICATION = "rectification"

    def __str__(self) -> str:
        return str(self.value)
