from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_peer_body import AddPeerBody
from ...models.error_response import ErrorResponse
from ...models.vpc_peer_json import VpcPeerJson
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: AddPeerBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/vpc/{id}/peers".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | VpcPeerJson | None:
    if response.status_code == 201:
        response_201 = VpcPeerJson.from_dict(response.json())

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
) -> Response[ErrorResponse | VpcPeerJson]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: AddPeerBody,
) -> Response[ErrorResponse | VpcPeerJson]:
    """Add a peer to a VPC.

     Registers a peer in the VPC. Currently returns 501 — peer
    enforcement and durable storage are a planned capability.

    Args:
        id (str):
        body (AddPeerBody): Request body for `POST /v1/vpc/{id}/peers`. Mirrors
            `scalix_vpc::AddPeerRequest`.
            Documentation-only (see `CreateVpcBody`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VpcPeerJson]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: AddPeerBody,
) -> ErrorResponse | VpcPeerJson | None:
    """Add a peer to a VPC.

     Registers a peer in the VPC. Currently returns 501 — peer
    enforcement and durable storage are a planned capability.

    Args:
        id (str):
        body (AddPeerBody): Request body for `POST /v1/vpc/{id}/peers`. Mirrors
            `scalix_vpc::AddPeerRequest`.
            Documentation-only (see `CreateVpcBody`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VpcPeerJson
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: AddPeerBody,
) -> Response[ErrorResponse | VpcPeerJson]:
    """Add a peer to a VPC.

     Registers a peer in the VPC. Currently returns 501 — peer
    enforcement and durable storage are a planned capability.

    Args:
        id (str):
        body (AddPeerBody): Request body for `POST /v1/vpc/{id}/peers`. Mirrors
            `scalix_vpc::AddPeerRequest`.
            Documentation-only (see `CreateVpcBody`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VpcPeerJson]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: AddPeerBody,
) -> ErrorResponse | VpcPeerJson | None:
    """Add a peer to a VPC.

     Registers a peer in the VPC. Currently returns 501 — peer
    enforcement and durable storage are a planned capability.

    Args:
        id (str):
        body (AddPeerBody): Request body for `POST /v1/vpc/{id}/peers`. Mirrors
            `scalix_vpc::AddPeerRequest`.
            Documentation-only (see `CreateVpcBody`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VpcPeerJson
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
