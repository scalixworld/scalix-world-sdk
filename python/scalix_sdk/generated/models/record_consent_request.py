from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecordConsentRequest")


@_attrs_define
class RecordConsentRequest:
    """Record a single consent decision (POST `/v1/auth/user/consent`).

    Attributes:
        consent_type (str):
        granted (bool):
    """

    consent_type: str
    granted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        consent_type = self.consent_type

        granted = self.granted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "consent_type": consent_type,
                "granted": granted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        consent_type = d.pop("consent_type")

        granted = d.pop("granted")

        record_consent_request = cls(
            consent_type=consent_type,
            granted=granted,
        )

        record_consent_request.additional_properties = d
        return record_consent_request

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
