from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IpRangesRequest")


@_attrs_define
class IpRangesRequest:
    """Request body for `PUT /v1/shield/crawlers/{id}/ip-ranges`.

    Attributes:
        ranges (list[str]): IP addresses or CIDR ranges used to verify the crawler's source IP.
    """

    ranges: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ranges = self.ranges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ranges": ranges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ranges = cast("list[str]", d.pop("ranges"))

        ip_ranges_request = cls(
            ranges=ranges,
        )

        ip_ranges_request.additional_properties = d
        return ip_ranges_request

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
