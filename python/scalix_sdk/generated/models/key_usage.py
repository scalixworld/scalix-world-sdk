from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="KeyUsage")


@_attrs_define
class KeyUsage:
    """One of the org's API keys with its real, IAM-tracked metadata.

    Note: per-key *request counts* are not tracked — metering is keyed by
    org/project (see docs/IDENTITY.md), not by individual key — so this returns
    the authoritative key metadata IAM holds (incl. `last_used_at`) rather than a
    fabricated request total. Org/project usage totals live at `/v1/usage/{id}`.

        Attributes:
            key_id (str): API key id (UUID).
            key_name (str): Human-friendly key name.
            key_prefix (str): Non-secret key prefix, e.g. `scalix_sk_ab12`.
            last_used_at (None | str | Unset): RFC3339 timestamp of the key's last use, or null if never used.
    """

    key_id: str
    key_name: str
    key_prefix: str
    last_used_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_id = self.key_id

        key_name = self.key_name

        key_prefix = self.key_prefix

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = self.last_used_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key_id": key_id,
                "key_name": key_name,
                "key_prefix": key_prefix,
            }
        )
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_id = d.pop("key_id")

        key_name = d.pop("key_name")

        key_prefix = d.pop("key_prefix")

        def _parse_last_used_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        key_usage = cls(
            key_id=key_id,
            key_name=key_name,
            key_prefix=key_prefix,
            last_used_at=last_used_at,
        )

        key_usage.additional_properties = d
        return key_usage

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
