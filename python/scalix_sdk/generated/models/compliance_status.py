from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.compliance_check import ComplianceCheck


T = TypeVar("T", bound="ComplianceStatus")


@_attrs_define
class ComplianceStatus:
    """
    Attributes:
        checks (list[ComplianceCheck]):
        passed (int):
        failed (int):
        score (float):
    """

    checks: list[ComplianceCheck]
    passed: int
    failed: int
    score: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        passed = self.passed

        failed = self.failed

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checks": checks,
                "passed": passed,
                "failed": failed,
                "score": score,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compliance_check import ComplianceCheck

        d = dict(src_dict)
        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = ComplianceCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        passed = d.pop("passed")

        failed = d.pop("failed")

        score = d.pop("score")

        compliance_status = cls(
            checks=checks,
            passed=passed,
            failed=failed,
            score=score,
        )

        compliance_status.additional_properties = d
        return compliance_status

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
