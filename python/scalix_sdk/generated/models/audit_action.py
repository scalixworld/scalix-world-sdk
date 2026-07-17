from enum import Enum


class AuditAction(str, Enum):
    API_KEY_CREATE = "api_key_create"
    API_KEY_REVOKE = "api_key_revoke"
    API_KEY_ROTATE = "api_key_rotate"
    AUTH_FAIL = "auth_fail"
    AUTH_LOGIN = "auth_login"
    COMPLIANCE_ERASURE = "compliance_erasure"
    COMPLIANCE_EXPORT = "compliance_export"
    CONFIG_CHANGE = "config_change"
    DATA_ACCESS = "data_access"
    DATA_DELETE = "data_delete"
    DATA_MODIFY = "data_modify"
    MEMBER_ADD = "member_add"
    MEMBER_REMOVE = "member_remove"

    def __str__(self) -> str:
        return str(self.value)
