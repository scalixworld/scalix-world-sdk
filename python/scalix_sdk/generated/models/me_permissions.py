from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MePermissions")


@_attrs_define
class MePermissions:
    """Effective permissions for the caller's token.

    Attributes:
        role (str):
        scopes (list[str]):
        can_create_keys (bool):
        can_create_projects (bool):
    """

    role: str
    scopes: list[str]
    can_create_keys: bool
    can_create_projects: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        scopes = self.scopes

        can_create_keys = self.can_create_keys

        can_create_projects = self.can_create_projects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "scopes": scopes,
                "can_create_keys": can_create_keys,
                "can_create_projects": can_create_projects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        scopes = cast("list[str]", d.pop("scopes"))

        can_create_keys = d.pop("can_create_keys")

        can_create_projects = d.pop("can_create_projects")

        me_permissions = cls(
            role=role,
            scopes=scopes,
            can_create_keys=can_create_keys,
            can_create_projects=can_create_projects,
        )

        me_permissions.additional_properties = d
        return me_permissions

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
