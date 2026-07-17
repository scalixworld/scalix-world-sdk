from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.kv_set_request_value import KvSetRequestValue


T = TypeVar("T", bound="KvSetRequest")


@_attrs_define
class KvSetRequest:
    """Set a key in the key-value store. The downstream kvstore accepts a JSON
    `value` of any shape; `ttl` is in seconds and optional.

        Attributes:
            key (str):
            value (KvSetRequestValue):
            ttl (int | None | Unset): Optional time-to-live in seconds.
    """

    key: str
    value: KvSetRequestValue
    ttl: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value.to_dict()

        ttl: int | None | Unset
        if isinstance(self.ttl, Unset):
            ttl = UNSET
        else:
            ttl = self.ttl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )
        if ttl is not UNSET:
            field_dict["ttl"] = ttl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kv_set_request_value import KvSetRequestValue

        d = dict(src_dict)
        key = d.pop("key")

        value = KvSetRequestValue.from_dict(d.pop("value"))

        def _parse_ttl(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        ttl = _parse_ttl(d.pop("ttl", UNSET))

        kv_set_request = cls(
            key=key,
            value=value,
            ttl=ttl,
        )

        kv_set_request.additional_properties = d
        return kv_set_request

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
