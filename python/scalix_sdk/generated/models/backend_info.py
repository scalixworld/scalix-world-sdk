from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BackendInfo")


@_attrs_define
class BackendInfo:
    """
    Attributes:
        id (UUID):
        url (str):
        weight (int):
        healthy (bool):
        active_conns (int):
    """

    id: UUID
    url: str
    weight: int
    healthy: bool
    active_conns: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        url = self.url

        weight = self.weight

        healthy = self.healthy

        active_conns = self.active_conns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "url": url,
                "weight": weight,
                "healthy": healthy,
                "active_conns": active_conns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        url = d.pop("url")

        weight = d.pop("weight")

        healthy = d.pop("healthy")

        active_conns = d.pop("active_conns")

        backend_info = cls(
            id=id,
            url=url,
            weight=weight,
            healthy=healthy,
            active_conns=active_conns,
        )

        backend_info.additional_properties = d
        return backend_info

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
