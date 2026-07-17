from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.integration_json import IntegrationJson


T = TypeVar("T", bound="CreateIntegrationResponse")


@_attrs_define
class CreateIntegrationResponse:
    """Response for `POST /v1/integrations` — the created integration plus the
    webhook URL and secret to configure on the provider.

        Attributes:
            integration (IntegrationJson): A source-control integration (GitHub/GitLab/Bitbucket) attached to a project.
            webhook_url (str):
            webhook_secret (str):
    """

    integration: IntegrationJson
    webhook_url: str
    webhook_secret: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration = self.integration.to_dict()

        webhook_url = self.webhook_url

        webhook_secret = self.webhook_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "integration": integration,
                "webhook_url": webhook_url,
                "webhook_secret": webhook_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_json import IntegrationJson

        d = dict(src_dict)
        integration = IntegrationJson.from_dict(d.pop("integration"))

        webhook_url = d.pop("webhook_url")

        webhook_secret = d.pop("webhook_secret")

        create_integration_response = cls(
            integration=integration,
            webhook_url=webhook_url,
            webhook_secret=webhook_secret,
        )

        create_integration_response.additional_properties = d
        return create_integration_response

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
