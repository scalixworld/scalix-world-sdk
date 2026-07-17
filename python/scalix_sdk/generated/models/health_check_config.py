from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HealthCheckConfig")


@_attrs_define
class HealthCheckConfig:
    """
    Attributes:
        interval_secs (int):
        timeout_secs (int):
        path (str):
        expected_status (int):
    """

    interval_secs: int
    timeout_secs: int
    path: str
    expected_status: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interval_secs = self.interval_secs

        timeout_secs = self.timeout_secs

        path = self.path

        expected_status = self.expected_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interval_secs": interval_secs,
                "timeout_secs": timeout_secs,
                "path": path,
                "expected_status": expected_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interval_secs = d.pop("interval_secs")

        timeout_secs = d.pop("timeout_secs")

        path = d.pop("path")

        expected_status = d.pop("expected_status")

        health_check_config = cls(
            interval_secs=interval_secs,
            timeout_secs=timeout_secs,
            path=path,
            expected_status=expected_status,
        )

        health_check_config.additional_properties = d
        return health_check_config

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
