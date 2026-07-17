from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scope_config_category_defaults import ScopeConfigCategoryDefaults


T = TypeVar("T", bound="ScopeConfig")


@_attrs_define
class ScopeConfig:
    """
    Attributes:
        enabled (bool | Unset):
        inject_noai_headers (bool | Unset): Adds `X-Robots-Tag: noai, noimageai` to proxied responses.
        tdm_reservation (bool | Unset): Adds `tdm-reservation: 1` (EU DSM Directive text-and-data-mining opt-out).
        block_impersonators (bool | Unset): Block crawlers whose source IP fails verification against configured
            ranges. Off by default: stale ranges must not break legitimate bots.
        category_defaults (ScopeConfigCategoryDefaults | Unset): Per-category default action, keyed by crawler category.
    """

    enabled: bool | Unset = UNSET
    inject_noai_headers: bool | Unset = UNSET
    tdm_reservation: bool | Unset = UNSET
    block_impersonators: bool | Unset = UNSET
    category_defaults: ScopeConfigCategoryDefaults | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        inject_noai_headers = self.inject_noai_headers

        tdm_reservation = self.tdm_reservation

        block_impersonators = self.block_impersonators

        category_defaults: dict[str, Any] | Unset = UNSET
        if not isinstance(self.category_defaults, Unset):
            category_defaults = self.category_defaults.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if inject_noai_headers is not UNSET:
            field_dict["inject_noai_headers"] = inject_noai_headers
        if tdm_reservation is not UNSET:
            field_dict["tdm_reservation"] = tdm_reservation
        if block_impersonators is not UNSET:
            field_dict["block_impersonators"] = block_impersonators
        if category_defaults is not UNSET:
            field_dict["category_defaults"] = category_defaults

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scope_config_category_defaults import ScopeConfigCategoryDefaults

        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        inject_noai_headers = d.pop("inject_noai_headers", UNSET)

        tdm_reservation = d.pop("tdm_reservation", UNSET)

        block_impersonators = d.pop("block_impersonators", UNSET)

        _category_defaults = d.pop("category_defaults", UNSET)
        category_defaults: ScopeConfigCategoryDefaults | Unset
        if isinstance(_category_defaults, Unset):
            category_defaults = UNSET
        else:
            category_defaults = ScopeConfigCategoryDefaults.from_dict(_category_defaults)

        scope_config = cls(
            enabled=enabled,
            inject_noai_headers=inject_noai_headers,
            tdm_reservation=tdm_reservation,
            block_impersonators=block_impersonators,
            category_defaults=category_defaults,
        )

        scope_config.additional_properties = d
        return scope_config

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
