from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compute_deploy_request_env_type_0 import ComputeDeployRequestEnvType0


T = TypeVar("T", bound="ComputeDeployRequest")


@_attrs_define
class ComputeDeployRequest:
    """Deploy a long-running compute service (container/VM).

    Attributes:
        name (str):
        image (str):
        cpu (int | None | Unset):
        memory_mb (int | None | Unset):
        env (ComputeDeployRequestEnvType0 | None | Unset): Environment variables (string → string).
        ports (list[int] | None | Unset):
        replicas (int | None | Unset):
    """

    name: str
    image: str
    cpu: int | None | Unset = UNSET
    memory_mb: int | None | Unset = UNSET
    env: ComputeDeployRequestEnvType0 | None | Unset = UNSET
    ports: list[int] | None | Unset = UNSET
    replicas: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.compute_deploy_request_env_type_0 import ComputeDeployRequestEnvType0

        name = self.name

        image = self.image

        cpu: int | None | Unset
        if isinstance(self.cpu, Unset):
            cpu = UNSET
        else:
            cpu = self.cpu

        memory_mb: int | None | Unset
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        env: dict[str, Any] | None | Unset
        if isinstance(self.env, Unset):
            env = UNSET
        elif isinstance(self.env, ComputeDeployRequestEnvType0):
            env = self.env.to_dict()
        else:
            env = self.env

        ports: list[int] | None | Unset
        if isinstance(self.ports, Unset):
            ports = UNSET
        elif isinstance(self.ports, list):
            ports = self.ports

        else:
            ports = self.ports

        replicas: int | None | Unset
        if isinstance(self.replicas, Unset):
            replicas = UNSET
        else:
            replicas = self.replicas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "image": image,
            }
        )
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if env is not UNSET:
            field_dict["env"] = env
        if ports is not UNSET:
            field_dict["ports"] = ports
        if replicas is not UNSET:
            field_dict["replicas"] = replicas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compute_deploy_request_env_type_0 import ComputeDeployRequestEnvType0

        d = dict(src_dict)
        name = d.pop("name")

        image = d.pop("image")

        def _parse_cpu(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        cpu = _parse_cpu(d.pop("cpu", UNSET))

        def _parse_memory_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        def _parse_env(data: object) -> ComputeDeployRequestEnvType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                env_type_0 = ComputeDeployRequestEnvType0.from_dict(data)

                return env_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("ComputeDeployRequestEnvType0 | None | Unset", data)

        env = _parse_env(d.pop("env", UNSET))

        def _parse_ports(data: object) -> list[int] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ports_type_0 = cast("list[int]", data)

                return ports_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast("list[int] | None | Unset", data)

        ports = _parse_ports(d.pop("ports", UNSET))

        def _parse_replicas(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast("int | None | Unset", data)

        replicas = _parse_replicas(d.pop("replicas", UNSET))

        compute_deploy_request = cls(
            name=name,
            image=image,
            cpu=cpu,
            memory_mb=memory_mb,
            env=env,
            ports=ports,
            replicas=replicas,
        )

        compute_deploy_request.additional_properties = d
        return compute_deploy_request

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
