from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """Standard error envelope every endpoint returns. Mirrors the body produced by
    `ApiError`'s `IntoResponse` in `server.rs` (`ApiError` itself can't derive
    `ToSchema` — it holds a `StatusCode`). Keep the field set in sync.

        Attributes:
            error (str): Human-readable error message. Example: Authentication required.
            code (str): Stable machine-readable code, e.g. `AUTH_FAILED`. Example: AUTH_FAILED.
            request_id (None | str | Unset): Correlation id for support.
            docs_url (None | str | Unset): Link to the relevant error docs.
            field (None | str | Unset): Offending field, for validation errors.
    """

    error: str
    code: str
    request_id: None | str | Unset = UNSET
    docs_url: None | str | Unset = UNSET
    field: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code

        request_id: None | str | Unset
        if isinstance(self.request_id, Unset):
            request_id = UNSET
        else:
            request_id = self.request_id

        docs_url: None | str | Unset
        if isinstance(self.docs_url, Unset):
            docs_url = UNSET
        else:
            docs_url = self.docs_url

        field: None | str | Unset
        if isinstance(self.field, Unset):
            field = UNSET
        else:
            field = self.field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "code": code,
            }
        )
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if docs_url is not UNSET:
            field_dict["docs_url"] = docs_url
        if field is not UNSET:
            field_dict["field"] = field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code")

        def _parse_request_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        request_id = _parse_request_id(d.pop("request_id", UNSET))

        def _parse_docs_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        docs_url = _parse_docs_url(d.pop("docs_url", UNSET))

        def _parse_field(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        field = _parse_field(d.pop("field", UNSET))

        error_response = cls(
            error=error,
            code=code,
            request_id=request_id,
            docs_url=docs_url,
            field=field,
        )

        error_response.additional_properties = d
        return error_response

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
