from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deleted_response import DeletedResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    id: str,
    backend_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/lb/{id}/backends/{backend_id}".format(
            id=quote(str(id), safe=""),
            backend_id=quote(str(backend_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeletedResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DeletedResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

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
) -> Response[DeletedResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    backend_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[DeletedResponse | ErrorResponse]:
    """Remove a backend from a load balancer.

     Deletes a backend target from the load balancer by id.

    Args:
        id (str):
        backend_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletedResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        backend_id=backend_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    backend_id: str,
    *,
    client: AuthenticatedClient,
) -> DeletedResponse | ErrorResponse | None:
    """Remove a backend from a load balancer.

     Deletes a backend target from the load balancer by id.

    Args:
        id (str):
        backend_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletedResponse | ErrorResponse
    """

    return sync_detailed(
        id=id,
        backend_id=backend_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    backend_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[DeletedResponse | ErrorResponse]:
    """Remove a backend from a load balancer.

     Deletes a backend target from the load balancer by id.

    Args:
        id (str):
        backend_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletedResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        backend_id=backend_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    backend_id: str,
    *,
    client: AuthenticatedClient,
) -> DeletedResponse | ErrorResponse | None:
    """Remove a backend from a load balancer.

     Deletes a backend target from the load balancer by id.

    Args:
        id (str):
        backend_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletedResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            backend_id=backend_id,
            client=client,
        )
    ).parsed
