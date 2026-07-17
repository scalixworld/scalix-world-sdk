from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waf_pattern_type_4_type import WafPatternType4Type

T = TypeVar("T", bound="WafPatternType4")


@_attrs_define
class WafPatternType4:
    """
    Attributes:
        window_secs (int):
        max_requests (int):
        type_ (WafPatternType4Type):
    """

    window_secs: int
    max_requests: int
    type_: WafPatternType4Type
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        window_secs = self.window_secs

        max_requests = self.max_requests

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "window_secs": window_secs,
                "max_requests": max_requests,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        window_secs = d.pop("window_secs")

        max_requests = d.pop("max_requests")

        type_ = WafPatternType4Type(d.pop("type"))

        waf_pattern_type_4 = cls(
            window_secs=window_secs,
            max_requests=max_requests,
            type_=type_,
        )

        waf_pattern_type_4.additional_properties = d
        return waf_pattern_type_4

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
