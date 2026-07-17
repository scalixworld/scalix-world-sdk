from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waf_pattern_type_2_type import WafPatternType2Type

T = TypeVar("T", bound="WafPatternType2")


@_attrs_define
class WafPatternType2:
    """
    Attributes:
        name (str):
        pattern (str):
        type_ (WafPatternType2Type):
    """

    name: str
    pattern: str
    type_: WafPatternType2Type
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        pattern = self.pattern

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "pattern": pattern,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        pattern = d.pop("pattern")

        type_ = WafPatternType2Type(d.pop("type"))

        waf_pattern_type_2 = cls(
            name=name,
            pattern=pattern,
            type_=type_,
        )

        waf_pattern_type_2.additional_properties = d
        return waf_pattern_type_2

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
