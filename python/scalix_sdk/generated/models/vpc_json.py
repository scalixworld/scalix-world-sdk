from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VpcJson")


@_attrs_define
class VpcJson:
    """A VPC. Mirrors `scalix_vpc::Vpc`.

    Attributes:
        id (str):
        tenant_id (str):
        name (str):
        cidr (str):
        private_key (str):
        public_key (str):
        listen_port (int):
        status (str): One of `provisioning`, `active`, `degraded`, `deleting`.
        created_at (str):
        endpoint (None | str | Unset):
    """

    id: str
    tenant_id: str
    name: str
    cidr: str
    private_key: str
    public_key: str
    listen_port: int
    status: str
    created_at: str
    endpoint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        name = self.name

        cidr = self.cidr

        private_key = self.private_key

        public_key = self.public_key

        listen_port = self.listen_port

        status = self.status

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
                "tenant_id": tenant_id,
                "name": name,
                "cidr": cidr,
                "private_key": private_key,
                "public_key": public_key,
                "listen_port": listen_port,
                "status": status,
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

        tenant_id = d.pop("tenant_id")

        name = d.pop("name")

        cidr = d.pop("cidr")

        private_key = d.pop("private_key")

        public_key = d.pop("public_key")

        listen_port = d.pop("listen_port")

        status = d.pop("status")

        created_at = d.pop("created_at")

        def _parse_endpoint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        vpc_json = cls(
            id=id,
            tenant_id=tenant_id,
            name=name,
            cidr=cidr,
            private_key=private_key,
            public_key=public_key,
            listen_port=listen_port,
            status=status,
            created_at=created_at,
            endpoint=endpoint,
        )

        vpc_json.additional_properties = d
        return vpc_json

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
