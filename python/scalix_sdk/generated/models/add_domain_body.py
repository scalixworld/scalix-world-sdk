from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddDomainBody")


@_attrs_define
class AddDomainBody:
    """Request body for `POST /v1/domains` — the custom domain to register.

    Attributes:
        domain (str): Fully-qualified domain to attach, e.g. `app.example.com`. Example: app.example.com.
        run_service (None | str | Unset): Optional Scalix Run service (by name) this domain should serve. When
            set, requests to the domain are proxied to the service exactly like
            `{name}.run.scalix.world`; when omitted, the domain serves the
            project's API surface. The service must belong to the caller's
            project. Example: my-frontend.
    """

    domain: str
    run_service: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain = self.domain

        run_service: None | str | Unset
        if isinstance(self.run_service, Unset):
            run_service = UNSET
        else:
            run_service = self.run_service

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
            }
        )
        if run_service is not UNSET:
            field_dict["run_service"] = run_service

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        domain = d.pop("domain")

        def _parse_run_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        run_service = _parse_run_service(d.pop("run_service", UNSET))

        add_domain_body = cls(
            domain=domain,
            run_service=run_service,
        )

        add_domain_body.additional_properties = d
        return add_domain_body

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
