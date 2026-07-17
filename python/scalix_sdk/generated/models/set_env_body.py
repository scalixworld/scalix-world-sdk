from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetEnvBody")


@_attrs_define
class SetEnvBody:
    """Request body for `POST /v1/env` — a single project environment variable.
    Fields are read by serde + utoipa; the 501-stub handlers ignore the body.

        Attributes:
            key (str):
            value (str):
            is_secret (bool | None | Unset): Store the value as a write-only secret (masked on read).
    """

    key: str
    value: str
    is_secret: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        is_secret: bool | None | Unset
        if isinstance(self.is_secret, Unset):
            is_secret = UNSET
        else:
            is_secret = self.is_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )
        if is_secret is not UNSET:
            field_dict["is_secret"] = is_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        value = d.pop("value")

        def _parse_is_secret(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("bool | None | Unset", data)

        is_secret = _parse_is_secret(d.pop("is_secret", UNSET))

        set_env_body = cls(
            key=key,
            value=value,
            is_secret=is_secret,
        )

        set_env_body.additional_properties = d
        return set_env_body

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
