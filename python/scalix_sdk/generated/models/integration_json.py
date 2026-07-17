from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationJson")


@_attrs_define
class IntegrationJson:
    """A source-control integration (GitHub/GitLab/Bitbucket) attached to a project.

    Attributes:
        id (str):
        project_id (str):
        provider (str):
        repo_url (str):
        branch_filter (str):
        auto_build (bool):
        auto_deploy (bool):
        status (str):
        preview_enabled (bool):
        preview_ttl_hours (int):
        created_at (str):
        updated_at (str):
        service_id (None | str | Unset):
    """

    id: str
    project_id: str
    provider: str
    repo_url: str
    branch_filter: str
    auto_build: bool
    auto_deploy: bool
    status: str
    preview_enabled: bool
    preview_ttl_hours: int
    created_at: str
    updated_at: str
    service_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        provider = self.provider

        repo_url = self.repo_url

        branch_filter = self.branch_filter

        auto_build = self.auto_build

        auto_deploy = self.auto_deploy

        status = self.status

        preview_enabled = self.preview_enabled

        preview_ttl_hours = self.preview_ttl_hours

        created_at = self.created_at

        updated_at = self.updated_at

        service_id: None | str | Unset
        if isinstance(self.service_id, Unset):
            service_id = UNSET
        else:
            service_id = self.service_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "provider": provider,
                "repo_url": repo_url,
                "branch_filter": branch_filter,
                "auto_build": auto_build,
                "auto_deploy": auto_deploy,
                "status": status,
                "preview_enabled": preview_enabled,
                "preview_ttl_hours": preview_ttl_hours,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if service_id is not UNSET:
            field_dict["service_id"] = service_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        provider = d.pop("provider")

        repo_url = d.pop("repo_url")

        branch_filter = d.pop("branch_filter")

        auto_build = d.pop("auto_build")

        auto_deploy = d.pop("auto_deploy")

        status = d.pop("status")

        preview_enabled = d.pop("preview_enabled")

        preview_ttl_hours = d.pop("preview_ttl_hours")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_service_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        service_id = _parse_service_id(d.pop("service_id", UNSET))

        integration_json = cls(
            id=id,
            project_id=project_id,
            provider=provider,
            repo_url=repo_url,
            branch_filter=branch_filter,
            auto_build=auto_build,
            auto_deploy=auto_deploy,
            status=status,
            preview_enabled=preview_enabled,
            preview_ttl_hours=preview_ttl_hours,
            created_at=created_at,
            updated_at=updated_at,
            service_id=service_id,
        )

        integration_json.additional_properties = d
        return integration_json

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
