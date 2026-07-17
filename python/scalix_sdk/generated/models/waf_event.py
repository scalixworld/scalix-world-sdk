from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waf_action import WafAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="WafEvent")


@_attrs_define
class WafEvent:
    """
    Attributes:
        id (UUID):
        rule_id (UUID):
        rule_name (str):
        action (WafAction):
        source_ip (str):
        path (str):
        reason (str):
        timestamp (datetime.datetime):
        tenant_id (str | Unset):
    """

    id: UUID
    rule_id: UUID
    rule_name: str
    action: WafAction
    source_ip: str
    path: str
    reason: str
    timestamp: datetime.datetime
    tenant_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        rule_id = str(self.rule_id)

        rule_name = self.rule_name

        action = self.action.value

        source_ip = self.source_ip

        path = self.path

        reason = self.reason

        timestamp = self.timestamp.isoformat()

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "rule_id": rule_id,
                "rule_name": rule_name,
                "action": action,
                "source_ip": source_ip,
                "path": path,
                "reason": reason,
                "timestamp": timestamp,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        rule_id = UUID(d.pop("rule_id"))

        rule_name = d.pop("rule_name")

        action = WafAction(d.pop("action"))

        source_ip = d.pop("source_ip")

        path = d.pop("path")

        reason = d.pop("reason")

        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        tenant_id = d.pop("tenant_id", UNSET)

        waf_event = cls(
            id=id,
            rule_id=rule_id,
            rule_name=rule_name,
            action=action,
            source_ip=source_ip,
            path=path,
            reason=reason,
            timestamp=timestamp,
            tenant_id=tenant_id,
        )

        waf_event.additional_properties = d
        return waf_event

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
