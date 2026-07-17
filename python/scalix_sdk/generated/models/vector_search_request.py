from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vector_search_request_filter_type_0 import VectorSearchRequestFilterType0


T = TypeVar("T", bound="VectorSearchRequest")


@_attrs_define
class VectorSearchRequest:
    """A nearest-neighbour vector search.

    Attributes:
        collection (str):
        query_vector (list[float]): The query embedding.
        top_k (int | None | Unset): Number of nearest neighbours to return.
        filter_ (None | Unset | VectorSearchRequestFilterType0): Optional metadata filter.
    """

    collection: str
    query_vector: list[float]
    top_k: int | None | Unset = UNSET
    filter_: None | Unset | VectorSearchRequestFilterType0 = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vector_search_request_filter_type_0 import VectorSearchRequestFilterType0

        collection = self.collection

        query_vector = self.query_vector

        top_k: int | None | Unset
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        filter_: dict[str, Any] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, VectorSearchRequestFilterType0):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
                "query_vector": query_vector,
            }
        )
        if top_k is not UNSET:
            field_dict["top_k"] = top_k
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vector_search_request_filter_type_0 import VectorSearchRequestFilterType0

        d = dict(src_dict)
        collection = d.pop("collection")

        query_vector = cast("list[float]", d.pop("query_vector"))

        def _parse_top_k(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        top_k = _parse_top_k(d.pop("top_k", UNSET))

        def _parse_filter_(data: object) -> None | Unset | VectorSearchRequestFilterType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = VectorSearchRequestFilterType0.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("None | Unset | VectorSearchRequestFilterType0", data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        vector_search_request = cls(
            collection=collection,
            query_vector=query_vector,
            top_k=top_k,
            filter_=filter_,
        )

        vector_search_request.additional_properties = d
        return vector_search_request

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
