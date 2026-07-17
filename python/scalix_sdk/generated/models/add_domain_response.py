from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.domain_instructions import DomainInstructions
    from ..models.domain_json import DomainJson


T = TypeVar("T", bound="AddDomainResponse")


@_attrs_define
class AddDomainResponse:
    """Response for `POST /v1/domains` — the created domain plus DNS setup steps.

    Attributes:
        domain (DomainJson): A custom domain attached to a project, with verification + SSL state.
        instructions (DomainInstructions): DNS setup steps returned when a domain is added.
    """

    domain: DomainJson
    instructions: DomainInstructions
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        domain = self.domain.to_dict()

        instructions = self.instructions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
                "instructions": instructions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.domain_instructions import DomainInstructions
        from ..models.domain_json import DomainJson

        d = dict(src_dict)
        domain = DomainJson.from_dict(d.pop("domain"))

        instructions = DomainInstructions.from_dict(d.pop("instructions"))

        add_domain_response = cls(
            domain=domain,
            instructions=instructions,
        )

        add_domain_response.additional_properties = d
        return add_domain_response

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
