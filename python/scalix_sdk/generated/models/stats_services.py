from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_stat import AiStat
    from ..models.bandwidth_stat import BandwidthStat
    from ..models.compute_stat import ComputeStat
    from ..models.functions_stat import FunctionsStat
    from ..models.storage_stat import StorageStat


T = TypeVar("T", bound="StatsServices")


@_attrs_define
class StatsServices:
    """Per-service usage breakdown.

    Attributes:
        ai (AiStat):
        storage (StorageStat):
        compute (ComputeStat):
        bandwidth (BandwidthStat):
        functions (FunctionsStat):
    """

    ai: AiStat
    storage: StorageStat
    compute: ComputeStat
    bandwidth: BandwidthStat
    functions: FunctionsStat
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ai = self.ai.to_dict()

        storage = self.storage.to_dict()

        compute = self.compute.to_dict()

        bandwidth = self.bandwidth.to_dict()

        functions = self.functions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ai": ai,
                "storage": storage,
                "compute": compute,
                "bandwidth": bandwidth,
                "functions": functions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_stat import AiStat
        from ..models.bandwidth_stat import BandwidthStat
        from ..models.compute_stat import ComputeStat
        from ..models.functions_stat import FunctionsStat
        from ..models.storage_stat import StorageStat

        d = dict(src_dict)
        ai = AiStat.from_dict(d.pop("ai"))

        storage = StorageStat.from_dict(d.pop("storage"))

        compute = ComputeStat.from_dict(d.pop("compute"))

        bandwidth = BandwidthStat.from_dict(d.pop("bandwidth"))

        functions = FunctionsStat.from_dict(d.pop("functions"))

        stats_services = cls(
            ai=ai,
            storage=storage,
            compute=compute,
            bandwidth=bandwidth,
            functions=functions,
        )

        stats_services.additional_properties = d
        return stats_services

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
