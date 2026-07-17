from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vector_entry_metadata_type_0 import VectorEntryMetadataType0


T = TypeVar("T", bound="VectorEntry")


@_attrs_define
class VectorEntry:
    """A single vector entry for upsert.

    Attributes:
        id (str):
        embedding (list[float]): The embedding values.
        metadata (None | Unset | VectorEntryMetadataType0):
    """

    id: str
    embedding: list[float]
    metadata: None | Unset | VectorEntryMetadataType0 = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vector_entry_metadata_type_0 import VectorEntryMetadataType0

        id = self.id

        embedding = self.embedding

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, VectorEntryMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "embedding": embedding,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vector_entry_metadata_type_0 import VectorEntryMetadataType0

        d = dict(src_dict)
        id = d.pop("id")

        embedding = cast("list[float]", d.pop("embedding"))

        def _parse_metadata(data: object) -> None | Unset | VectorEntryMetadataType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = VectorEntryMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("None | Unset | VectorEntryMetadataType0", data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        vector_entry = cls(
            id=id,
            embedding=embedding,
            metadata=metadata,
        )

        vector_entry.additional_properties = d
        return vector_entry

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
