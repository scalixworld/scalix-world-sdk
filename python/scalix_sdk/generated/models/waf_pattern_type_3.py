from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waf_pattern_type_3_type import WafPatternType3Type

T = TypeVar("T", bound="WafPatternType3")


@_attrs_define
class WafPatternType3:
    """
    Attributes:
        max_bytes (int):
        type_ (WafPatternType3Type):
    """

    max_bytes: int
    type_: WafPatternType3Type
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_bytes = self.max_bytes

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_bytes": max_bytes,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_bytes = d.pop("max_bytes")

        type_ = WafPatternType3Type(d.pop("type"))

        waf_pattern_type_3 = cls(
            max_bytes=max_bytes,
            type_=type_,
        )

        waf_pattern_type_3.additional_properties = d
        return waf_pattern_type_3

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
