from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BudgetUsage")


@_attrs_define
class BudgetUsage:
    """Usage figures (floats) — used for the current usage and remaining allowance.

    Attributes:
        ai_tokens (float):
        storage_gb (float):
        compute_hours (float):
    """

    ai_tokens: float
    storage_gb: float
    compute_hours: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ai_tokens = self.ai_tokens

        storage_gb = self.storage_gb

        compute_hours = self.compute_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ai_tokens": ai_tokens,
                "storage_gb": storage_gb,
                "compute_hours": compute_hours,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ai_tokens = d.pop("ai_tokens")

        storage_gb = d.pop("storage_gb")

        compute_hours = d.pop("compute_hours")

        budget_usage = cls(
            ai_tokens=ai_tokens,
            storage_gb=storage_gb,
            compute_hours=compute_hours,
        )

        budget_usage.additional_properties = d
        return budget_usage

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
