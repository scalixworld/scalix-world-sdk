from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.installation_json import InstallationJson


T = TypeVar("T", bound="ListInstallationsResponse")


@_attrs_define
class ListInstallationsResponse:
    """Response for `GET /v1/integrations/github/installations`.

    Attributes:
        installations (list[InstallationJson]):
    """

    installations: list[InstallationJson]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        installations = []
        for installations_item_data in self.installations:
            installations_item = installations_item_data.to_dict()
            installations.append(installations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "installations": installations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.installation_json import InstallationJson

        d = dict(src_dict)
        installations = []
        _installations = d.pop("installations")
        for installations_item_data in _installations:
            installations_item = InstallationJson.from_dict(installations_item_data)

            installations.append(installations_item)

        list_installations_response = cls(
            installations=installations,
        )

        list_installations_response.additional_properties = d
        return list_installations_response

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
