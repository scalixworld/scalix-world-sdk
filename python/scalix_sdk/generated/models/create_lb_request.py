from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.strategy import Strategy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_backend_request import AddBackendRequest
    from ..models.health_check_config import HealthCheckConfig


T = TypeVar("T", bound="CreateLbRequest")


@_attrs_define
class CreateLbRequest:
    """
    Attributes:
        name (str):
        strategy (Strategy | Unset):
        backends (list[AddBackendRequest] | Unset):
        health_check (HealthCheckConfig | None | Unset):
    """

    name: str
    strategy: Strategy | Unset = UNSET
    backends: list[AddBackendRequest] | Unset = UNSET
    health_check: HealthCheckConfig | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.health_check_config import HealthCheckConfig

        name = self.name

        strategy: str | Unset = UNSET
        if not isinstance(self.strategy, Unset):
            strategy = self.strategy.value

        backends: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.backends, Unset):
            backends = []
            for backends_item_data in self.backends:
                backends_item = backends_item_data.to_dict()
                backends.append(backends_item)

        health_check: dict[str, Any] | None | Unset
        if isinstance(self.health_check, Unset):
            health_check = UNSET
        elif isinstance(self.health_check, HealthCheckConfig):
            health_check = self.health_check.to_dict()
        else:
            health_check = self.health_check

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if strategy is not UNSET:
            field_dict["strategy"] = strategy
        if backends is not UNSET:
            field_dict["backends"] = backends
        if health_check is not UNSET:
            field_dict["health_check"] = health_check

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_backend_request import AddBackendRequest
        from ..models.health_check_config import HealthCheckConfig

        d = dict(src_dict)
        name = d.pop("name")

        _strategy = d.pop("strategy", UNSET)
        strategy: Strategy | Unset
        if isinstance(_strategy, Unset):
            strategy = UNSET
        else:
            strategy = Strategy(_strategy)

        _backends = d.pop("backends", UNSET)
        backends: list[AddBackendRequest] | Unset = UNSET
        if _backends is not UNSET:
            backends = []
            for backends_item_data in _backends:
                backends_item = AddBackendRequest.from_dict(backends_item_data)

                backends.append(backends_item)

        def _parse_health_check(data: object) -> HealthCheckConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                health_check_type_1 = HealthCheckConfig.from_dict(data)

                return health_check_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("HealthCheckConfig | None | Unset", data)

        health_check = _parse_health_check(d.pop("health_check", UNSET))

        create_lb_request = cls(
            name=name,
            strategy=strategy,
            backends=backends,
            health_check=health_check,
        )

        create_lb_request.additional_properties = d
        return create_lb_request

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
