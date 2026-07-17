from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DomainJson")


@_attrs_define
class DomainJson:
    """A custom domain attached to a project, with verification + SSL state.

    Attributes:
        id (str):
        project_id (str):
        domain (str):
        domain_type (str):
        status (str):
        verification_token (str):
        ssl_status (str):
        ssl_expires_at (str):
        ssl_issued_at (str):
        primary_domain (bool):
        created_at (str):
        updated_at (str):
        ssl_error (None | str | Unset): Last cert-issuance failure reason (absent = none). Lets the console show
            "DNS doesn't point to our edge" instead of a silent stuck 'none'/'failed'.
        cname_target (None | str | Unset):
        run_service (None | str | Unset): Run service this domain serves (absent = the project's API surface).
    """

    id: str
    project_id: str
    domain: str
    domain_type: str
    status: str
    verification_token: str
    ssl_status: str
    ssl_expires_at: str
    ssl_issued_at: str
    primary_domain: bool
    created_at: str
    updated_at: str
    ssl_error: None | str | Unset = UNSET
    cname_target: None | str | Unset = UNSET
    run_service: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        domain = self.domain

        domain_type = self.domain_type

        status = self.status

        verification_token = self.verification_token

        ssl_status = self.ssl_status

        ssl_expires_at = self.ssl_expires_at

        ssl_issued_at = self.ssl_issued_at

        primary_domain = self.primary_domain

        created_at = self.created_at

        updated_at = self.updated_at

        ssl_error: None | str | Unset
        if isinstance(self.ssl_error, Unset):
            ssl_error = UNSET
        else:
            ssl_error = self.ssl_error

        cname_target: None | str | Unset
        if isinstance(self.cname_target, Unset):
            cname_target = UNSET
        else:
            cname_target = self.cname_target

        run_service: None | str | Unset
        if isinstance(self.run_service, Unset):
            run_service = UNSET
        else:
            run_service = self.run_service

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "domain": domain,
                "domain_type": domain_type,
                "status": status,
                "verification_token": verification_token,
                "ssl_status": ssl_status,
                "ssl_expires_at": ssl_expires_at,
                "ssl_issued_at": ssl_issued_at,
                "primary_domain": primary_domain,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if ssl_error is not UNSET:
            field_dict["ssl_error"] = ssl_error
        if cname_target is not UNSET:
            field_dict["cname_target"] = cname_target
        if run_service is not UNSET:
            field_dict["run_service"] = run_service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        domain = d.pop("domain")

        domain_type = d.pop("domain_type")

        status = d.pop("status")

        verification_token = d.pop("verification_token")

        ssl_status = d.pop("ssl_status")

        ssl_expires_at = d.pop("ssl_expires_at")

        ssl_issued_at = d.pop("ssl_issued_at")

        primary_domain = d.pop("primary_domain")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        def _parse_ssl_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        ssl_error = _parse_ssl_error(d.pop("ssl_error", UNSET))

        def _parse_cname_target(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        cname_target = _parse_cname_target(d.pop("cname_target", UNSET))

        def _parse_run_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        run_service = _parse_run_service(d.pop("run_service", UNSET))

        domain_json = cls(
            id=id,
            project_id=project_id,
            domain=domain,
            domain_type=domain_type,
            status=status,
            verification_token=verification_token,
            ssl_status=ssl_status,
            ssl_expires_at=ssl_expires_at,
            ssl_issued_at=ssl_issued_at,
            primary_domain=primary_domain,
            created_at=created_at,
            updated_at=updated_at,
            ssl_error=ssl_error,
            cname_target=cname_target,
            run_service=run_service,
        )

        domain_json.additional_properties = d
        return domain_json

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
