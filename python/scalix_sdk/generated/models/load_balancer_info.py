from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.strategy import Strategy

if TYPE_CHECKING:
    from ..models.backend_info import BackendInfo


T = TypeVar("T", bound="LoadBalancerInfo")


@_attrs_define
class LoadBalancerInfo:
    """
    Attributes:
        id (UUID):
        name (str):
        strategy (Strategy):
        backends (list[BackendInfo]):
        created_at (datetime.datetime):
    """

    id: UUID
    name: str
    strategy: Strategy
    backends: list[BackendInfo]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        strategy = self.strategy.value

        backends = []
        for backends_item_data in self.backends:
            backends_item = backends_item_data.to_dict()
            backends.append(backends_item)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "strategy": strategy,
                "backends": backends,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backend_info import BackendInfo

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        strategy = Strategy(d.pop("strategy"))

        backends = []
        _backends = d.pop("backends")
        for backends_item_data in _backends:
            backends_item = BackendInfo.from_dict(backends_item_data)

            backends.append(backends_item)

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        load_balancer_info = cls(
            id=id,
            name=name,
            strategy=strategy,
            backends=backends,
            created_at=created_at,
        )

        load_balancer_info.additional_properties = d
        return load_balancer_info

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
