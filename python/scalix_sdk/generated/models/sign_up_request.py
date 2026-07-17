from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sign_up_request_data_type_0 import SignUpRequestDataType0


T = TypeVar("T", bound="SignUpRequest")


@_attrs_define
class SignUpRequest:
    """New-account signup payload.

    Attributes:
        email (str):
        password (str):
        data (None | SignUpRequestDataType0 | Unset): Arbitrary user metadata to attach to the account.
        captcha_token (None | str | Unset):
    """

    email: str
    password: str
    data: None | SignUpRequestDataType0 | Unset = UNSET
    captcha_token: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sign_up_request_data_type_0 import SignUpRequestDataType0

        email = self.email

        password = self.password

        data: dict[str, Any] | None | Unset
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, SignUpRequestDataType0):
            data = self.data.to_dict()
        else:
            data = self.data

        captcha_token: None | str | Unset
        if isinstance(self.captcha_token, Unset):
            captcha_token = UNSET
        else:
            captcha_token = self.captcha_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if captcha_token is not UNSET:
            field_dict["captcha_token"] = captcha_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sign_up_request_data_type_0 import SignUpRequestDataType0

        d = dict(src_dict)
        email = d.pop("email")

        password = d.pop("password")

        def _parse_data(data: object) -> None | SignUpRequestDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = SignUpRequestDataType0.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("None | SignUpRequestDataType0 | Unset", data)

        data = _parse_data(d.pop("data", UNSET))

        def _parse_captcha_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        captcha_token = _parse_captcha_token(d.pop("captcha_token", UNSET))

        sign_up_request = cls(
            email=email,
            password=password,
            data=data,
            captcha_token=captcha_token,
        )

        sign_up_request.additional_properties = d
        return sign_up_request

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
