from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserInfo")


@_attrs_define
class UserInfo:
    """Account profile for the caller (`GET /v1/user/info`). Fields after `status`
    are present only when the user record exists.

        Attributes:
            id (str):
            plan (str):
            status (str):
            email (None | str | Unset): Account email; `null` for an unknown user.
            name (None | str | Unset): Display name; `null` if unset/unknown.
            login_count (int | None | Unset):
            created_at (None | str | Unset):
            last_login_at (None | str | Unset):
    """

    id: str
    plan: str
    status: str
    email: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    login_count: int | None | Unset = UNSET
    created_at: None | str | Unset = UNSET
    last_login_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        plan = self.plan

        status = self.status

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        login_count: int | None | Unset
        if isinstance(self.login_count, Unset):
            login_count = UNSET
        else:
            login_count = self.login_count

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        last_login_at: None | str | Unset
        if isinstance(self.last_login_at, Unset):
            last_login_at = UNSET
        else:
            last_login_at = self.last_login_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "plan": plan,
                "status": status,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if name is not UNSET:
            field_dict["name"] = name
        if login_count is not UNSET:
            field_dict["login_count"] = login_count
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if last_login_at is not UNSET:
            field_dict["last_login_at"] = last_login_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        plan = d.pop("plan")

        status = d.pop("status")

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_login_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        login_count = _parse_login_count(d.pop("login_count", UNSET))

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_last_login_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        last_login_at = _parse_last_login_at(d.pop("last_login_at", UNSET))

        user_info = cls(
            id=id,
            plan=plan,
            status=status,
            email=email,
            name=name,
            login_count=login_count,
            created_at=created_at,
            last_login_at=last_login_at,
        )

        user_info.additional_properties = d
        return user_info

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
