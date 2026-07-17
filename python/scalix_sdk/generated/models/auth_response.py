from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user import User


T = TypeVar("T", bound="AuthResponse")


@_attrs_define
class AuthResponse:
    """Authentication tokens plus the authenticated user.

    Attributes:
        access_token (str):
        refresh_token (str):
        expires_in (int):
        expires_at (datetime.datetime):
        token_type (str):  Example: bearer.
        user (User): An end-user account.
    """

    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: datetime.datetime
    token_type: str
    user: User
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        refresh_token = self.refresh_token

        expires_in = self.expires_in

        expires_at = self.expires_at.isoformat()

        token_type = self.token_type

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": expires_in,
                "expires_at": expires_at,
                "token_type": token_type,
                "user": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user import User

        d = dict(src_dict)
        access_token = d.pop("access_token")

        refresh_token = d.pop("refresh_token")

        expires_in = d.pop("expires_in")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        token_type = d.pop("token_type")

        user = User.from_dict(d.pop("user"))

        auth_response = cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            expires_at=expires_at,
            token_type=token_type,
            user=user,
        )

        auth_response.additional_properties = d
        return auth_response

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
