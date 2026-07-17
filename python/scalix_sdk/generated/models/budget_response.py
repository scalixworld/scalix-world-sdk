from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.budget_limits import BudgetLimits
    from ..models.budget_usage import BudgetUsage


T = TypeVar("T", bound="BudgetResponse")


@_attrs_define
class BudgetResponse:
    """Response for `GET /v1/user/budget`.

    Attributes:
        user_id (str):
        usage (BudgetUsage): Usage figures (floats) — used for the current usage and remaining allowance.
        limits (BudgetLimits): Plan allowances.
        remaining (BudgetUsage): Usage figures (floats) — used for the current usage and remaining allowance.
    """

    user_id: str
    usage: BudgetUsage
    limits: BudgetLimits
    remaining: BudgetUsage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        usage = self.usage.to_dict()

        limits = self.limits.to_dict()

        remaining = self.remaining.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "usage": usage,
                "limits": limits,
                "remaining": remaining,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.budget_limits import BudgetLimits
        from ..models.budget_usage import BudgetUsage

        d = dict(src_dict)
        user_id = d.pop("user_id")

        usage = BudgetUsage.from_dict(d.pop("usage"))

        limits = BudgetLimits.from_dict(d.pop("limits"))

        remaining = BudgetUsage.from_dict(d.pop("remaining"))

        budget_response = cls(
            user_id=user_id,
            usage=usage,
            limits=limits,
            remaining=remaining,
        )

        budget_response.additional_properties = d
        return budget_response

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
