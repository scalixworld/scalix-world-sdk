from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gdpr_request_type import GdprRequestType
from ..models.request_status import RequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataSubjectRequest")


@_attrs_define
class DataSubjectRequest:
    """
    Attributes:
        id (UUID):
        tenant_id (str):
        subject_email (str):
        request_type (GdprRequestType):
        status (RequestStatus):
        created_at (datetime.datetime):
        notes (None | str | Unset):
        completed_at (datetime.datetime | None | Unset):
    """

    id: UUID
    tenant_id: str
    subject_email: str
    request_type: GdprRequestType
    status: RequestStatus
    created_at: datetime.datetime
    notes: None | str | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        tenant_id = self.tenant_id

        subject_email = self.subject_email

        request_type = self.request_type.value

        status = self.status.value

        created_at = self.created_at.isoformat()

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tenant_id": tenant_id,
                "subject_email": subject_email,
                "request_type": request_type,
                "status": status,
                "created_at": created_at,
            }
        )
        if notes is not UNSET:
            field_dict["notes"] = notes
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        tenant_id = d.pop("tenant_id")

        subject_email = d.pop("subject_email")

        request_type = GdprRequestType(d.pop("request_type"))

        status = RequestStatus(d.pop("status"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("datetime.datetime | None | Unset", data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        data_subject_request = cls(
            id=id,
            tenant_id=tenant_id,
            subject_email=subject_email,
            request_type=request_type,
            status=status,
            created_at=created_at,
            notes=notes,
            completed_at=completed_at,
        )

        data_subject_request.additional_properties = d
        return data_subject_request

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
