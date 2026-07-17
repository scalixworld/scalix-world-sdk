from enum import Enum


class Strategy(str, Enum):
    IP_HASH = "ip_hash"
    LEAST_CONNECTIONS = "least_connections"
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"

    def __str__(self) -> str:
        return str(self.value)
