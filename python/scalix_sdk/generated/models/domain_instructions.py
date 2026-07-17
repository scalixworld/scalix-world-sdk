from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DomainInstructions")


@_attrs_define
class DomainInstructions:
    """DNS setup steps returned when a domain is added.

    Attributes:
        step_1 (str):
        step_2 (str):
        step_3 (str):
        step_4 (str):
    """

    step_1: str
    step_2: str
    step_3: str
    step_4: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step_1 = self.step_1

        step_2 = self.step_2

        step_3 = self.step_3

        step_4 = self.step_4

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_1": step_1,
                "step_2": step_2,
                "step_3": step_3,
                "step_4": step_4,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step_1 = d.pop("step_1")

        step_2 = d.pop("step_2")

        step_3 = d.pop("step_3")

        step_4 = d.pop("step_4")

        domain_instructions = cls(
            step_1=step_1,
            step_2=step_2,
            step_3=step_3,
            step_4=step_4,
        )

        domain_instructions.additional_properties = d
        return domain_instructions

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
