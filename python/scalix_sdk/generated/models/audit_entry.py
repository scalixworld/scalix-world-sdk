from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.audit_action import AuditAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditEntry")


@_attrs_define
class AuditEntry:
    """
    Attributes:
        id (UUID):
        timestamp (datetime.datetime):
        tenant_id (str):
        actor (str):
        action (AuditAction):
        resource (str):
        source_ip (str):
        details (None | str | Unset):
        request_id (None | str | Unset):
        entry_hash (str | Unset):
        prev_hash (str | Unset):
    """

    id: UUID
    timestamp: datetime.datetime
    tenant_id: str
    actor: str
    action: AuditAction
    resource: str
    source_ip: str
    details: None | str | Unset = UNSET
    request_id: None | str | Unset = UNSET
    entry_hash: str | Unset = UNSET
    prev_hash: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        timestamp = self.timestamp.isoformat()

        tenant_id = self.tenant_id

        actor = self.actor

        action = self.action.value

        resource = self.resource

        source_ip = self.source_ip

        details: None | str | Unset
        if isinstance(self.details, Unset):
            details = UNSET
        else:
            details = self.details

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        entry_hash = self.entry_hash

        prev_hash = self.prev_hash

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "timestamp": timestamp,
                "tenant_id": tenant_id,
                "actor": actor,
                "action": action,
                "resource": resource,
                "source_ip": source_ip,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if entry_hash is not UNSET:
            field_dict["entry_hash"] = entry_hash
        if prev_hash is not UNSET:
            field_dict["prev_hash"] = prev_hash

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        tenant_id = d.pop("tenant_id")

        actor = d.pop("actor")

        action = AuditAction(d.pop("action"))

        resource = d.pop("resource")

        source_ip = d.pop("source_ip")

        def _parse_details(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        details = _parse_details(d.pop("details", UNSET))

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        entry_hash = d.pop("entry_hash", UNSET)

        prev_hash = d.pop("prev_hash", UNSET)

        audit_entry = cls(
            id=id,
            timestamp=timestamp,
            tenant_id=tenant_id,
            actor=actor,
            action=action,
            resource=resource,
            source_ip=source_ip,
            details=details,
            request_id=request_id,
            entry_hash=entry_hash,
            prev_hash=prev_hash,
        )

        audit_entry.additional_properties = d
        return audit_entry

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
