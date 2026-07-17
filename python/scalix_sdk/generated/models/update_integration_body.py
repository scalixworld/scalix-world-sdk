from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateIntegrationBody")


@_attrs_define
class UpdateIntegrationBody:
    """Request body for `PUT /v1/integrations/{id}`.

    Attributes:
        branch_filter (None | str | Unset):
        auto_build (bool | None | Unset):
        auto_deploy (bool | None | Unset):
        service_id (None | str | Unset):
        preview_enabled (bool | None | Unset):
        preview_ttl_hours (int | None | Unset):
        status (None | str | Unset):
    """

    branch_filter: None | str | Unset = UNSET
    auto_build: bool | None | Unset = UNSET
    auto_deploy: bool | None | Unset = UNSET
    service_id: None | str | Unset = UNSET
    preview_enabled: bool | None | Unset = UNSET
    preview_ttl_hours: int | None | Unset = UNSET
    status: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        branch_filter: None | str | Unset
        if isinstance(self.branch_filter, Unset):
            branch_filter = UNSET
        else:
            branch_filter = self.branch_filter

        auto_build: bool | None | Unset
        if isinstance(self.auto_build, Unset):
            auto_build = UNSET
        else:
            auto_build = self.auto_build

        auto_deploy: bool | None | Unset
        if isinstance(self.auto_deploy, Unset):
            auto_deploy = UNSET
        else:
            auto_deploy = self.auto_deploy

        service_id: None | str | Unset
        if isinstance(self.service_id, Unset):
            service_id = UNSET
        else:
            service_id = self.service_id

        preview_enabled: bool | None | Unset
        if isinstance(self.preview_enabled, Unset):
            preview_enabled = UNSET
        else:
            preview_enabled = self.preview_enabled

        preview_ttl_hours: int | None | Unset
        if isinstance(self.preview_ttl_hours, Unset):
            preview_ttl_hours = UNSET
        else:
            preview_ttl_hours = self.preview_ttl_hours

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if branch_filter is not UNSET:
            field_dict["branch_filter"] = branch_filter
        if auto_build is not UNSET:
            field_dict["auto_build"] = auto_build
        if auto_deploy is not UNSET:
            field_dict["auto_deploy"] = auto_deploy
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if preview_enabled is not UNSET:
            field_dict["preview_enabled"] = preview_enabled
        if preview_ttl_hours is not UNSET:
            field_dict["preview_ttl_hours"] = preview_ttl_hours
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_branch_filter(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        branch_filter = _parse_branch_filter(d.pop("branch_filter", UNSET))

        def _parse_auto_build(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("bool | None | Unset", data)

        auto_build = _parse_auto_build(d.pop("auto_build", UNSET))

        def _parse_auto_deploy(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("bool | None | Unset", data)

        auto_deploy = _parse_auto_deploy(d.pop("auto_deploy", UNSET))

        def _parse_service_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        service_id = _parse_service_id(d.pop("service_id", UNSET))

        def _parse_preview_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("bool | None | Unset", data)

        preview_enabled = _parse_preview_enabled(d.pop("preview_enabled", UNSET))

        def _parse_preview_ttl_hours(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        preview_ttl_hours = _parse_preview_ttl_hours(d.pop("preview_ttl_hours", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        status = _parse_status(d.pop("status", UNSET))

        update_integration_body = cls(
            branch_filter=branch_filter,
            auto_build=auto_build,
            auto_deploy=auto_deploy,
            service_id=service_id,
            preview_enabled=preview_enabled,
            preview_ttl_hours=preview_ttl_hours,
            status=status,
        )

        update_integration_body.additional_properties = d
        return update_integration_body

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
