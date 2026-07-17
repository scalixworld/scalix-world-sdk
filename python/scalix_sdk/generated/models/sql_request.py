from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sql_request_params_type_0 import SqlRequestParamsType0


T = TypeVar("T", bound="SqlRequest")


@_attrs_define
class SqlRequest:
    """A parameterized SQL query to execute against the tenant's database.

    Attributes:
        query (str): The SQL statement, with `$1`, `$2`, … placeholders for params. Example: SELECT * FROM users WHERE
            id = $1.
        params (None | SqlRequestParamsType0 | Unset): Positional bind parameters for the placeholders, in order.
    """

    query: str
    params: None | SqlRequestParamsType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sql_request_params_type_0 import SqlRequestParamsType0

        query = self.query

        params: dict[str, Any] | None | Unset
        if isinstance(self.params, Unset):
            params = UNSET
        elif isinstance(self.params, SqlRequestParamsType0):
            params = self.params.to_dict()
        else:
            params = self.params

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sql_request_params_type_0 import SqlRequestParamsType0

        d = dict(src_dict)
        query = d.pop("query")

        def _parse_params(data: object) -> None | SqlRequestParamsType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_0 = SqlRequestParamsType0.from_dict(data)

                return params_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("None | SqlRequestParamsType0 | Unset", data)

        params = _parse_params(d.pop("params", UNSET))

        sql_request = cls(
            query=query,
            params=params,
        )

        sql_request.additional_properties = d
        return sql_request

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
