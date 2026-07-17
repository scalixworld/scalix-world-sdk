from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VpcPeerJson")


@_attrs_define
class VpcPeerJson:
    """A peer in a VPC. Mirrors `scalix_vpc::VpcPeer`.

    Attributes:
        id (str):
        vpc_id (str):
        name (str):
        public_key (str):
        allowed_ips (list[str]):
        persistent_keepalive (int):
        created_at (str):
        endpoint (None | str | Unset):
    """

    id: str
    vpc_id: str
    name: str
    public_key: str
    allowed_ips: list[str]
    persistent_keepalive: int
    created_at: str
    endpoint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        vpc_id = self.vpc_id

        name = self.name

        public_key = self.public_key

        allowed_ips = self.allowed_ips

        persistent_keepalive = self.persistent_keepalive

        created_at = self.created_at

        endpoint: None | str | Unset
        if isinstance(self.endpoint, Unset):
            endpoint = UNSET
        else:
            endpoint = self.endpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "vpc_id": vpc_id,
                "name": name,
                "public_key": public_key,
                "allowed_ips": allowed_ips,
                "persistent_keepalive": persistent_keepalive,
                "created_at": created_at,
            }
        )
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        vpc_id = d.pop("vpc_id")

        name = d.pop("name")

        public_key = d.pop("public_key")

        allowed_ips = cast("list[str]", d.pop("allowed_ips"))

        persistent_keepalive = d.pop("persistent_keepalive")

        created_at = d.pop("created_at")

        def _parse_endpoint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        vpc_peer_json = cls(
            id=id,
            vpc_id=vpc_id,
            name=name,
            public_key=public_key,
            allowed_ips=allowed_ips,
            persistent_keepalive=persistent_keepalive,
            created_at=created_at,
            endpoint=endpoint,
        )

        vpc_peer_json.additional_properties = d
        return vpc_peer_json

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
