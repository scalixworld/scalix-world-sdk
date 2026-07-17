from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MeIdentity")


@_attrs_define
class MeIdentity:
    """Token identity (key, type, tenancy, creator).

    Attributes:
        key_id (str):
        token_type (str):
        org_id (str):
        created_by (str):
        project_id (None | str | Unset):
    """

    key_id: str
    token_type: str
    org_id: str
    created_by: str
    project_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_id = self.key_id

        token_type = self.token_type

        org_id = self.org_id

        created_by = self.created_by

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key_id": key_id,
                "token_type": token_type,
                "org_id": org_id,
                "created_by": created_by,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_id = d.pop("key_id")

        token_type = d.pop("token_type")

        org_id = d.pop("org_id")

        created_by = d.pop("created_by")

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        me_identity = cls(
            key_id=key_id,
            token_type=token_type,
            org_id=org_id,
            created_by=created_by,
            project_id=project_id,
        )

        me_identity.additional_properties = d
        return me_identity

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
