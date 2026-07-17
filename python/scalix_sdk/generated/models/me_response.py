from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.me_identity import MeIdentity
    from ..models.me_limits import MeLimits
    from ..models.me_permissions import MePermissions


T = TypeVar("T", bound="MeResponse")


@_attrs_define
class MeResponse:
    """Response for `GET /v1/me` — identity, permissions, available MCP tools, limits.

    Attributes:
        identity (MeIdentity): Token identity (key, type, tenancy, creator).
        permissions (MePermissions): Effective permissions for the caller's token.
        tools (list[str]):
        limits (MeLimits): Plan-derived limits (advisory — see `api_key_limit_for_plan`/`rate_limit_for_plan`).
    """

    identity: MeIdentity
    permissions: MePermissions
    tools: list[str]
    limits: MeLimits
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identity = self.identity.to_dict()

        permissions = self.permissions.to_dict()

        tools = self.tools

        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identity": identity,
                "permissions": permissions,
                "tools": tools,
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.me_identity import MeIdentity
        from ..models.me_limits import MeLimits
        from ..models.me_permissions import MePermissions

        d = dict(src_dict)
        identity = MeIdentity.from_dict(d.pop("identity"))

        permissions = MePermissions.from_dict(d.pop("permissions"))

        tools = cast("list[str]", d.pop("tools"))

        limits = MeLimits.from_dict(d.pop("limits"))

        me_response = cls(
            identity=identity,
            permissions=permissions,
            tools=tools,
            limits=limits,
        )

        me_response.additional_properties = d
        return me_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
