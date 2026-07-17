from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_vpc_body import CreateVpcBody
from ...models.error_response import ErrorResponse
from ...models.vpc_json import VpcJson
from ...types import Response


def _get_kwargs(
    *,
    body: CreateVpcBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/vpc",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | VpcJson | None:
    if response.status_code == 201:
        response_201 = VpcJson.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if response.status_code == 501:
        response_501 = ErrorResponse.from_dict(response.json())

        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | VpcJson]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateVpcBody,
) -> Response[ErrorResponse | VpcJson]:
    """Create a VPC.

     Provisions a VPC for the caller's project. Currently returns 501 —
    enforcement and durable storage are a planned capability.

    Args:
        body (CreateVpcBody): Request body for `POST /v1/vpc`. Mirrors
            `scalix_vpc::CreateVpcRequest`.
            Documentation-only: the handler deserializes the external type directly, so
            these fields are read by utoipa, not by runtime code.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VpcJson]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateVpcBody,
) -> ErrorResponse | VpcJson | None:
    """Create a VPC.

     Provisions a VPC for the caller's project. Currently returns 501 —
    enforcement and durable storage are a planned capability.

    Args:
        body (CreateVpcBody): Request body for `POST /v1/vpc`. Mirrors
            `scalix_vpc::CreateVpcRequest`.
            Documentation-only: the handler deserializes the external type directly, so
            these fields are read by utoipa, not by runtime code.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VpcJson
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateVpcBody,
) -> Response[ErrorResponse | VpcJson]:
    """Create a VPC.

     Provisions a VPC for the caller's project. Currently returns 501 —
    enforcement and durable storage are a planned capability.

    Args:
        body (CreateVpcBody): Request body for `POST /v1/vpc`. Mirrors
            `scalix_vpc::CreateVpcRequest`.
            Documentation-only: the handler deserializes the external type directly, so
            these fields are read by utoipa, not by runtime code.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VpcJson]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateVpcBody,
) -> ErrorResponse | VpcJson | None:
    """Create a VPC.

     Provisions a VPC for the caller's project. Currently returns 501 —
    enforcement and durable storage are a planned capability.

    Args:
        body (CreateVpcBody): Request body for `POST /v1/vpc`. Mirrors
            `scalix_vpc::CreateVpcRequest`.
            Documentation-only: the handler deserializes the external type directly, so
            these fields are read by utoipa, not by runtime code.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VpcJson
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
