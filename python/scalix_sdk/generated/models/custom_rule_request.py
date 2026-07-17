from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shield_action import ShieldAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomRuleRequest")


@_attrs_define
class CustomRuleRequest:
    """Request body for `POST /v1/shield/custom` — a customer-defined UA rule.
    The `CrawlerPolicy` fields (`action`, `rate_limit_per_min`) are flattened
    into the top level alongside `name` and `ua_pattern`.

        Attributes:
            action (ShieldAction):
            name (str):
            ua_pattern (str): Case-insensitive substring matched against the User-Agent header.
            rate_limit_per_min (int | None | Unset):
    """

    action: ShieldAction
    name: str
    ua_pattern: str
    rate_limit_per_min: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        name = self.name

        ua_pattern = self.ua_pattern

        rate_limit_per_min: int | None | Unset
        if isinstance(self.rate_limit_per_min, Unset):
            rate_limit_per_min = UNSET
        else:
            rate_limit_per_min = self.rate_limit_per_min

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "name": name,
                "ua_pattern": ua_pattern,
            }
        )
        if rate_limit_per_min is not UNSET:
            field_dict["rate_limit_per_min"] = rate_limit_per_min

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = ShieldAction(d.pop("action"))

        name = d.pop("name")

        ua_pattern = d.pop("ua_pattern")

        def _parse_rate_limit_per_min(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        rate_limit_per_min = _parse_rate_limit_per_min(d.pop("rate_limit_per_min", UNSET))

        custom_rule_request = cls(
            action=action,
            name=name,
            ua_pattern=ua_pattern,
            rate_limit_per_min=rate_limit_per_min,
        )

        custom_rule_request.additional_properties = d
        return custom_rule_request

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
