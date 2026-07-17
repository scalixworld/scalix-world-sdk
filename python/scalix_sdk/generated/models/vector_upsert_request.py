from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vector_entry import VectorEntry


T = TypeVar("T", bound="VectorUpsertRequest")


@_attrs_define
class VectorUpsertRequest:
    """Upsert a batch of vectors into a collection.

    Attributes:
        collection (str):
        entries (list[VectorEntry]):
    """

    collection: str
    entries: list[VectorEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        collection = self.collection

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vector_entry import VectorEntry

        d = dict(src_dict)
        collection = d.pop("collection")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = VectorEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        vector_upsert_request = cls(
            collection=collection,
            entries=entries,
        )

        vector_upsert_request.additional_properties = d
        return vector_upsert_request

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
