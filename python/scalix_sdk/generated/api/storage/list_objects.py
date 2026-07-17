from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    bucket: str,
    *,
    prefix: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["prefix"] = prefix

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/storage/buckets/{bucket}/objects".format(
            bucket=quote(str(bucket), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = cast("Any", None)
        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    bucket: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """List objects.

     Returns the objects in a bucket, optionally filtered by key prefix.

    Args:
        bucket (str):
        prefix (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        prefix=prefix,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    bucket: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """List objects.

     Returns the objects in a bucket, optionally filtered by key prefix.

    Args:
        bucket (str):
        prefix (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return sync_detailed(
        bucket=bucket,
        client=client,
        prefix=prefix,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    bucket: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | ErrorResponse]:
    """List objects.

     Returns the objects in a bucket, optionally filtered by key prefix.

    Args:
        bucket (str):
        prefix (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        prefix=prefix,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    bucket: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | ErrorResponse | None:
    """List objects.

     Returns the objects in a bucket, optionally filtered by key prefix.

    Args:
        bucket (str):
        prefix (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse
    """

    return (
        await asyncio_detailed(
            bucket=bucket,
            client=client,
            prefix=prefix,
            limit=limit,
        )
    ).parsed
