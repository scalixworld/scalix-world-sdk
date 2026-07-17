from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_deploy_request_env_type_0 import FunctionDeployRequestEnvType0


T = TypeVar("T", bound="FunctionDeployRequest")


@_attrs_define
class FunctionDeployRequest:
    """Deploy a serverless function.

    Attributes:
        name (str):
        runtime (str): One of `node`, `python`, `go`, `rust`. Example: node.
        image_ref (str):
        entry_point (None | str | Unset):
        handler (None | str | Unset):
        env (FunctionDeployRequestEnvType0 | None | Unset): Environment variables for the function (string → string).
        timeout_ms (int | None | Unset):
        memory_mb (int | None | Unset):
        cron_expression (None | str | Unset):
        http_trigger (bool | None | Unset):
    """

    name: str
    runtime: str
    image_ref: str
    entry_point: None | str | Unset = UNSET
    handler: None | str | Unset = UNSET
    env: FunctionDeployRequestEnvType0 | None | Unset = UNSET
    timeout_ms: int | None | Unset = UNSET
    memory_mb: int | None | Unset = UNSET
    cron_expression: None | str | Unset = UNSET
    http_trigger: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.function_deploy_request_env_type_0 import FunctionDeployRequestEnvType0

        name = self.name

        runtime = self.runtime

        image_ref = self.image_ref

        entry_point: None | str | Unset
        if isinstance(self.entry_point, Unset):
            entry_point = UNSET
        else:
            entry_point = self.entry_point

        handler: None | str | Unset
        if isinstance(self.handler, Unset):
            handler = UNSET
        else:
            handler = self.handler

        env: dict[str, Any] | None | Unset
        if isinstance(self.env, Unset):
            env = UNSET
        elif isinstance(self.env, FunctionDeployRequestEnvType0):
            env = self.env.to_dict()
        else:
            env = self.env

        timeout_ms: int | None | Unset
        if isinstance(self.timeout_ms, Unset):
            timeout_ms = UNSET
        else:
            timeout_ms = self.timeout_ms

        memory_mb: int | None | Unset
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        cron_expression: None | str | Unset
        if isinstance(self.cron_expression, Unset):
            cron_expression = UNSET
        else:
            cron_expression = self.cron_expression

        http_trigger: bool | None | Unset
        if isinstance(self.http_trigger, Unset):
            http_trigger = UNSET
        else:
            http_trigger = self.http_trigger

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "runtime": runtime,
                "image_ref": image_ref,
            }
        )
        if entry_point is not UNSET:
            field_dict["entry_point"] = entry_point
        if handler is not UNSET:
            field_dict["handler"] = handler
        if env is not UNSET:
            field_dict["env"] = env
        if timeout_ms is not UNSET:
            field_dict["timeout_ms"] = timeout_ms
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if cron_expression is not UNSET:
            field_dict["cron_expression"] = cron_expression
        if http_trigger is not UNSET:
            field_dict["http_trigger"] = http_trigger

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.function_deploy_request_env_type_0 import FunctionDeployRequestEnvType0

        d = dict(src_dict)
        name = d.pop("name")

        runtime = d.pop("runtime")

        image_ref = d.pop("image_ref")

        def _parse_entry_point(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        entry_point = _parse_entry_point(d.pop("entry_point", UNSET))

        def _parse_handler(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        handler = _parse_handler(d.pop("handler", UNSET))

        def _parse_env(data: object) -> FunctionDeployRequestEnvType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_type_0 = FunctionDeployRequestEnvType0.from_dict(data)

                return env_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("FunctionDeployRequestEnvType0 | None | Unset", data)

        env = _parse_env(d.pop("env", UNSET))

        def _parse_timeout_ms(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        timeout_ms = _parse_timeout_ms(d.pop("timeout_ms", UNSET))

        def _parse_memory_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        def _parse_cron_expression(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("None | str | Unset", data)

        cron_expression = _parse_cron_expression(d.pop("cron_expression", UNSET))

        def _parse_http_trigger(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("bool | None | Unset", data)

        http_trigger = _parse_http_trigger(d.pop("http_trigger", UNSET))

        function_deploy_request = cls(
            name=name,
            runtime=runtime,
            image_ref=image_ref,
            entry_point=entry_point,
            handler=handler,
            env=env,
            timeout_ms=timeout_ms,
            memory_mb=memory_mb,
            cron_expression=cron_expression,
            http_trigger=http_trigger,
        )

        function_deploy_request.additional_properties = d
        return function_deploy_request

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
