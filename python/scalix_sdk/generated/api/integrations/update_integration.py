from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.integration_response import IntegrationResponse
from ...models.update_integration_body import UpdateIntegrationBody
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: UpdateIntegrationBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/integrations/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | IntegrationResponse | None:
    if response.status_code == 200:
        response_200 = IntegrationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | IntegrationResponse]:
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
    body: UpdateIntegrationBody,
) -> Response[ErrorResponse | IntegrationResponse]:
    """Update a source-control integration.

     Updates an integration's build/deploy settings (branch filter, auto-build,
    auto-deploy, preview, status) and returns the updated record.

    Args:
        id (str):
        body (UpdateIntegrationBody): Request body for `PUT /v1/integrations/{id}`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IntegrationResponse]
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
    body: UpdateIntegrationBody,
) -> ErrorResponse | IntegrationResponse | None:
    """Update a source-control integration.

     Updates an integration's build/deploy settings (branch filter, auto-build,
    auto-deploy, preview, status) and returns the updated record.

    Args:
        id (str):
        body (UpdateIntegrationBody): Request body for `PUT /v1/integrations/{id}`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IntegrationResponse
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
    body: UpdateIntegrationBody,
) -> Response[ErrorResponse | IntegrationResponse]:
    """Update a source-control integration.

     Updates an integration's build/deploy settings (branch filter, auto-build,
    auto-deploy, preview, status) and returns the updated record.

    Args:
        id (str):
        body (UpdateIntegrationBody): Request body for `PUT /v1/integrations/{id}`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IntegrationResponse]
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
    body: UpdateIntegrationBody,
) -> ErrorResponse | IntegrationResponse | None:
    """Update a source-control integration.

     Updates an integration's build/deploy settings (branch filter, auto-build,
    auto-deploy, preview, status) and returns the updated record.

    Args:
        id (str):
        body (UpdateIntegrationBody): Request body for `PUT /v1/integrations/{id}`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IntegrationResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
