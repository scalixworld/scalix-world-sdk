from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_app_metadata import UserAppMetadata
    from ..models.user_user_metadata import UserUserMetadata


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """An end-user account.

    Attributes:
        id (UUID):
        email (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        user_metadata (UserUserMetadata):
        app_metadata (UserAppMetadata):
        phone (None | str | Unset):
        email_confirmed_at (datetime.datetime | None | Unset):
        last_sign_in_at (datetime.datetime | None | Unset):
    """

    id: UUID
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_metadata: UserUserMetadata
    app_metadata: UserAppMetadata
    phone: None | str | Unset = UNSET
    email_confirmed_at: datetime.datetime | None | Unset = UNSET
    last_sign_in_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        email = self.email

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        user_metadata = self.user_metadata.to_dict()

        app_metadata = self.app_metadata.to_dict()

        phone: None | str | Unset
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        email_confirmed_at: None | str | Unset
        if isinstance(self.email_confirmed_at, Unset):
            email_confirmed_at = UNSET
        elif isinstance(self.email_confirmed_at, datetime.datetime):
            email_confirmed_at = self.email_confirmed_at.isoformat()
        else:
            email_confirmed_at = self.email_confirmed_at

        last_sign_in_at: None | str | Unset
        if isinstance(self.last_sign_in_at, Unset):
            last_sign_in_at = UNSET
        elif isinstance(self.last_sign_in_at, datetime.datetime):
            last_sign_in_at = self.last_sign_in_at.isoformat()
        else:
            last_sign_in_at = self.last_sign_in_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "created_at": created_at,
                "updated_at": updated_at,
                "user_metadata": user_metadata,
                "app_metadata": app_metadata,
            }
        )
        if phone is not UNSET:
            field_dict["phone"] = phone
        if email_confirmed_at is not UNSET:
            field_dict["email_confirmed_at"] = email_confirmed_at
        if last_sign_in_at is not UNSET:
            field_dict["last_sign_in_at"] = last_sign_in_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_app_metadata import UserAppMetadata
        from ..models.user_user_metadata import UserUserMetadata

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        email = d.pop("email")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        user_metadata = UserUserMetadata.from_dict(d.pop("user_metadata"))

        app_metadata = UserAppMetadata.from_dict(d.pop("app_metadata"))

        def _parse_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_email_confirmed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                email_confirmed_at_type_0 = datetime.datetime.fromisoformat(data)

                return email_confirmed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("datetime.datetime | None | Unset", data)

        email_confirmed_at = _parse_email_confirmed_at(d.pop("email_confirmed_at", UNSET))

        def _parse_last_sign_in_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sign_in_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_sign_in_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("datetime.datetime | None | Unset", data)

        last_sign_in_at = _parse_last_sign_in_at(d.pop("last_sign_in_at", UNSET))

        user = cls(
            id=id,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
            user_metadata=user_metadata,
            app_metadata=app_metadata,
            phone=phone,
            email_confirmed_at=email_confirmed_at,
            last_sign_in_at=last_sign_in_at,
        )

        user.additional_properties = d
        return user

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
