from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WafStats")


@_attrs_define
class WafStats:
    """
    Attributes:
        total_requests (int):
        blocked_requests (int):
        blocked_24h (int):
        logged_requests (int):
        top_blocked_ips (list[list[int | str]]): `[ip, count]` pairs, highest first.
        top_rules (list[list[int | str]]): `[rule_name, count]` pairs, highest first.
        rules_count (int):
    """

    total_requests: int
    blocked_requests: int
    blocked_24h: int
    logged_requests: int
    top_blocked_ips: list[list[int | str]]
    top_rules: list[list[int | str]]
    rules_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_requests = self.total_requests

        blocked_requests = self.blocked_requests

        blocked_24h = self.blocked_24h

        logged_requests = self.logged_requests

        top_blocked_ips = []
        for top_blocked_ips_item_data in self.top_blocked_ips:
            top_blocked_ips_item = []
            for top_blocked_ips_item_item_data in top_blocked_ips_item_data:
                top_blocked_ips_item_item: int | str
                top_blocked_ips_item_item = top_blocked_ips_item_item_data
                top_blocked_ips_item.append(top_blocked_ips_item_item)

            top_blocked_ips.append(top_blocked_ips_item)

        top_rules = []
        for top_rules_item_data in self.top_rules:
            top_rules_item = []
            for top_rules_item_item_data in top_rules_item_data:
                top_rules_item_item: int | str
                top_rules_item_item = top_rules_item_item_data
                top_rules_item.append(top_rules_item_item)

            top_rules.append(top_rules_item)

        rules_count = self.rules_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_requests": total_requests,
                "blocked_requests": blocked_requests,
                "blocked_24h": blocked_24h,
                "logged_requests": logged_requests,
                "top_blocked_ips": top_blocked_ips,
                "top_rules": top_rules,
                "rules_count": rules_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_requests = d.pop("total_requests")

        blocked_requests = d.pop("blocked_requests")

        blocked_24h = d.pop("blocked_24h")

        logged_requests = d.pop("logged_requests")

        top_blocked_ips = []
        _top_blocked_ips = d.pop("top_blocked_ips")
        for top_blocked_ips_item_data in _top_blocked_ips:
            top_blocked_ips_item = []
            _top_blocked_ips_item = top_blocked_ips_item_data
            for top_blocked_ips_item_item_data in _top_blocked_ips_item:

                def _parse_top_blocked_ips_item_item(data: object) -> int | str:
                    return cast("int | str", data)

                top_blocked_ips_item_item = _parse_top_blocked_ips_item_item(
                    top_blocked_ips_item_item_data
                )

                top_blocked_ips_item.append(top_blocked_ips_item_item)

            top_blocked_ips.append(top_blocked_ips_item)

        top_rules = []
        _top_rules = d.pop("top_rules")
        for top_rules_item_data in _top_rules:
            top_rules_item = []
            _top_rules_item = top_rules_item_data
            for top_rules_item_item_data in _top_rules_item:

                def _parse_top_rules_item_item(data: object) -> int | str:
                    return cast("int | str", data)

                top_rules_item_item = _parse_top_rules_item_item(top_rules_item_item_data)

                top_rules_item.append(top_rules_item_item)

            top_rules.append(top_rules_item)

        rules_count = d.pop("rules_count")

        waf_stats = cls(
            total_requests=total_requests,
            blocked_requests=blocked_requests,
            blocked_24h=blocked_24h,
            logged_requests=logged_requests,
            top_blocked_ips=top_blocked_ips,
            top_rules=top_rules,
            rules_count=rules_count,
        )

        waf_stats.additional_properties = d
        return waf_stats

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
