from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddPeerBody")


@_attrs_define
class AddPeerBody:
    """Request body for `POST /v1/vpc/{id}/peers`. Mirrors `scalix_vpc::AddPeerRequest`.
    Documentation-only (see `CreateVpcBody`).

        Attributes:
            name (str):
            public_key (str):
            allowed_ips (list[str]):
            endpoint (None | str | Unset):
    """

    name: str
    public_key: str
    allowed_ips: list[str]
    endpoint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        public_key = self.public_key

        allowed_ips = self.allowed_ips

        endpoint: None | str | Unset
        if isinstance(self.endpoint, Unset):
            endpoint = UNSET
        else:
            endpoint = self.endpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "public_key": public_key,
                "allowed_ips": allowed_ips,
            }
        )
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        public_key = d.pop("public_key")

        allowed_ips = cast("list[str]", d.pop("allowed_ips"))

        def _parse_endpoint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        add_peer_body = cls(
            name=name,
            public_key=public_key,
            allowed_ips=allowed_ips,
            endpoint=endpoint,
        )

        add_peer_body.additional_properties = d
        return add_peer_body

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
