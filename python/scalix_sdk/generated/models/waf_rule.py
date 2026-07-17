from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.waf_action import WafAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.waf_pattern_type_0 import WafPatternType0
    from ..models.waf_pattern_type_1 import WafPatternType1
    from ..models.waf_pattern_type_2 import WafPatternType2
    from ..models.waf_pattern_type_3 import WafPatternType3
    from ..models.waf_pattern_type_4 import WafPatternType4
    from ..models.waf_pattern_type_5 import WafPatternType5
    from ..models.waf_pattern_type_6 import WafPatternType6
    from ..models.waf_pattern_type_7 import WafPatternType7


T = TypeVar("T", bound="WafRule")


@_attrs_define
class WafRule:
    """
    Attributes:
        id (UUID):
        name (str):
        pattern (WafPatternType0 | WafPatternType1 | WafPatternType2 | WafPatternType3 | WafPatternType4 |
            WafPatternType5 | WafPatternType6 | WafPatternType7):
        action (WafAction):
        priority (int):
        enabled (bool):
        tenant_id (str | Unset): Owning project/tenant. SEC-2: rules and their enforcement are scoped to
            this — a rule is only ever applied to its own tenant's traffic, and only
            its owner can see/update/delete it.
    """

    id: UUID
    name: str
    pattern: (
        WafPatternType0
        | WafPatternType1
        | WafPatternType2
        | WafPatternType3
        | WafPatternType4
        | WafPatternType5
        | WafPatternType6
        | WafPatternType7
    )
    action: WafAction
    priority: int
    enabled: bool
    tenant_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.waf_pattern_type_0 import WafPatternType0
        from ..models.waf_pattern_type_1 import WafPatternType1
        from ..models.waf_pattern_type_2 import WafPatternType2
        from ..models.waf_pattern_type_3 import WafPatternType3
        from ..models.waf_pattern_type_4 import WafPatternType4
        from ..models.waf_pattern_type_5 import WafPatternType5
        from ..models.waf_pattern_type_6 import WafPatternType6

        id = str(self.id)

        name = self.name

        pattern: dict[str, Any]
        if (
            isinstance(self.pattern, WafPatternType0)
            or isinstance(self.pattern, WafPatternType1)
            or isinstance(self.pattern, WafPatternType2)
            or isinstance(self.pattern, WafPatternType3)
            or isinstance(self.pattern, WafPatternType4)
            or isinstance(self.pattern, WafPatternType5)
            or isinstance(self.pattern, WafPatternType6)
        ):
            pattern = self.pattern.to_dict()
        else:
            pattern = self.pattern.to_dict()

        action = self.action.value

        priority = self.priority

        enabled = self.enabled

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "pattern": pattern,
                "action": action,
                "priority": priority,
                "enabled": enabled,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.waf_pattern_type_0 import WafPatternType0
        from ..models.waf_pattern_type_1 import WafPatternType1
        from ..models.waf_pattern_type_2 import WafPatternType2
        from ..models.waf_pattern_type_3 import WafPatternType3
        from ..models.waf_pattern_type_4 import WafPatternType4
        from ..models.waf_pattern_type_5 import WafPatternType5
        from ..models.waf_pattern_type_6 import WafPatternType6
        from ..models.waf_pattern_type_7 import WafPatternType7

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        def _parse_pattern(
            data: object,
        ) -> (
            WafPatternType0
            | WafPatternType1
            | WafPatternType2
            | WafPatternType3
            | WafPatternType4
            | WafPatternType5
            | WafPatternType6
            | WafPatternType7
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_0 = WafPatternType0.from_dict(data)

                return componentsschemas_waf_pattern_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_1 = WafPatternType1.from_dict(data)

                return componentsschemas_waf_pattern_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_2 = WafPatternType2.from_dict(data)

                return componentsschemas_waf_pattern_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_3 = WafPatternType3.from_dict(data)

                return componentsschemas_waf_pattern_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_4 = WafPatternType4.from_dict(data)

                return componentsschemas_waf_pattern_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_5 = WafPatternType5.from_dict(data)

                return componentsschemas_waf_pattern_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_waf_pattern_type_6 = WafPatternType6.from_dict(data)

                return componentsschemas_waf_pattern_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_waf_pattern_type_7 = WafPatternType7.from_dict(data)

            return componentsschemas_waf_pattern_type_7

        pattern = _parse_pattern(d.pop("pattern"))

        action = WafAction(d.pop("action"))

        priority = d.pop("priority")

        enabled = d.pop("enabled")

        tenant_id = d.pop("tenant_id", UNSET)

        waf_rule = cls(
            id=id,
            name=name,
            pattern=pattern,
            action=action,
            priority=priority,
            enabled=enabled,
            tenant_id=tenant_id,
        )

        waf_rule.additional_properties = d
        return waf_rule

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
