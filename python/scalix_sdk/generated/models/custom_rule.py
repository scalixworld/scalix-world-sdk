from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.crawler_policy import CrawlerPolicy


T = TypeVar("T", bound="CustomRule")


@_attrs_define
class CustomRule:
    """Customer-defined user-agent rule. Takes precedence over the built-in
    crawler database so customers can police bots we don't know about yet —
    or override how a known bot is matched.

        Attributes:
            id (UUID):
            name (str):
            ua_pattern (str): Case-insensitive substring matched against the User-Agent header.
            policy (CrawlerPolicy):
            created_at (datetime.datetime):
    """

    id: UUID
    name: str
    ua_pattern: str
    policy: CrawlerPolicy
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        ua_pattern = self.ua_pattern

        policy = self.policy.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "ua_pattern": ua_pattern,
                "policy": policy,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.crawler_policy import CrawlerPolicy

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        ua_pattern = d.pop("ua_pattern")

        policy = CrawlerPolicy.from_dict(d.pop("policy"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        custom_rule = cls(
            id=id,
            name=name,
            ua_pattern=ua_pattern,
            policy=policy,
            created_at=created_at,
        )

        custom_rule.additional_properties = d
        return custom_rule

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
