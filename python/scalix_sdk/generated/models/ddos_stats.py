from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DdosStats")


@_attrs_define
class DdosStats:
    """
    Attributes:
        global_rps (int):
        tracked_ips (int):
        blocked_ips (list[str]):
        threshold_rps (int):
        global_threshold (int):
    """

    global_rps: int
    tracked_ips: int
    blocked_ips: list[str]
    threshold_rps: int
    global_threshold: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        global_rps = self.global_rps

        tracked_ips = self.tracked_ips

        blocked_ips = self.blocked_ips

        threshold_rps = self.threshold_rps

        global_threshold = self.global_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "global_rps": global_rps,
                "tracked_ips": tracked_ips,
                "blocked_ips": blocked_ips,
                "threshold_rps": threshold_rps,
                "global_threshold": global_threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        global_rps = d.pop("global_rps")

        tracked_ips = d.pop("tracked_ips")

        blocked_ips = cast("list[str]", d.pop("blocked_ips"))

        threshold_rps = d.pop("threshold_rps")

        global_threshold = d.pop("global_threshold")

        ddos_stats = cls(
            global_rps=global_rps,
            tracked_ips=tracked_ips,
            blocked_ips=blocked_ips,
            threshold_rps=threshold_rps,
            global_threshold=global_threshold,
        )

        ddos_stats.additional_properties = d
        return ddos_stats

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
