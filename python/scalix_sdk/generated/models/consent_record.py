from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConsentRecord")


@_attrs_define
class ConsentRecord:
    """A recorded GDPR consent decision.

    Attributes:
        id (UUID):
        consent_type (str):  Example: data_processing.
        granted (bool):
        recorded_at (datetime.datetime):
        ip_address (None | str | Unset):
    """

    id: UUID
    consent_type: str
    granted: bool
    recorded_at: datetime.datetime
    ip_address: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        consent_type = self.consent_type

        granted = self.granted

        recorded_at = self.recorded_at.isoformat()

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "consent_type": consent_type,
                "granted": granted,
                "recorded_at": recorded_at,
            }
        )
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        consent_type = d.pop("consent_type")

        granted = d.pop("granted")

        recorded_at = datetime.datetime.fromisoformat(d.pop("recorded_at"))

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        consent_record = cls(
            id=id,
            consent_type=consent_type,
            granted=granted,
            recorded_at=recorded_at,
            ip_address=ip_address,
        )

        consent_record.additional_properties = d
        return consent_record

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
