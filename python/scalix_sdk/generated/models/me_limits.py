from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MeLimits")


@_attrs_define
class MeLimits:
    """Plan-derived limits (advisory — see `api_key_limit_for_plan`/`rate_limit_for_plan`).

    Attributes:
        plan (str):
        rate_limit_rps (int):
        api_keys_max (int):
    """

    plan: str
    rate_limit_rps: int
    api_keys_max: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        rate_limit_rps = self.rate_limit_rps

        api_keys_max = self.api_keys_max

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
                "rate_limit_rps": rate_limit_rps,
                "api_keys_max": api_keys_max,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan = d.pop("plan")

        rate_limit_rps = d.pop("rate_limit_rps")

        api_keys_max = d.pop("api_keys_max")

        me_limits = cls(
            plan=plan,
            rate_limit_rps=rate_limit_rps,
            api_keys_max=api_keys_max,
        )

        me_limits.additional_properties = d
        return me_limits

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
