from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_env_body import SetEnvBody


T = TypeVar("T", bound="BulkImportBody")


@_attrs_define
class BulkImportBody:
    """Request body for `POST /v1/env/bulk` — import many variables at once.

    Attributes:
        variables (list[SetEnvBody]):
    """

    variables: list[SetEnvBody]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        variables = []
        for variables_item_data in self.variables:
            variables_item = variables_item_data.to_dict()
            variables.append(variables_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "variables": variables,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_env_body import SetEnvBody

        d = dict(src_dict)
        variables = []
        _variables = d.pop("variables")
        for variables_item_data in _variables:
            variables_item = SetEnvBody.from_dict(variables_item_data)

            variables.append(variables_item)

        bulk_import_body = cls(
            variables=variables,
        )

        bulk_import_body.additional_properties = d
        return bulk_import_body

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
