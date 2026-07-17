from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ddos_stats import DdosStats
    from ..models.waf_stats import WafStats


T = TypeVar("T", bound="WafStatsResponse")


@_attrs_define
class WafStatsResponse:
    """Combined WAF + DDoS statistics for `GET /v1/waf/stats`.

    Attributes:
        waf (WafStats):
        ddos (DdosStats):
    """

    waf: WafStats
    ddos: DdosStats
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        waf = self.waf.to_dict()

        ddos = self.ddos.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "waf": waf,
                "ddos": ddos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ddos_stats import DdosStats
        from ..models.waf_stats import WafStats

        d = dict(src_dict)
        waf = WafStats.from_dict(d.pop("waf"))

        ddos = DdosStats.from_dict(d.pop("ddos"))

        waf_stats_response = cls(
            waf=waf,
            ddos=ddos,
        )

        waf_stats_response.additional_properties = d
        return waf_stats_response

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
