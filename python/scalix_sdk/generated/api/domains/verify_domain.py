from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.verify_domain_response import VerifyDomainResponse
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/domains/{id}/verify".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | VerifyDomainResponse | None:
    if response.status_code == 200:
        response_200 = VerifyDomainResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | VerifyDomainResponse]:
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
) -> Response[ErrorResponse | VerifyDomainResponse]:
    r"""Verify a custom domain.

     Confirms — via a standard public DNS lookup, no provider credentials — that the
    customer's domain points at our edge (its A records match `cname.<platform>`,
    or a configured `SCALIX_EDGE_IP`). On success, marks the domain active. This is
    the industry-standard \"does it point at us\" check (Vercel/Netlify/Render).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VerifyDomainResponse]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | VerifyDomainResponse | None:
    r"""Verify a custom domain.

     Confirms — via a standard public DNS lookup, no provider credentials — that the
    customer's domain points at our edge (its A records match `cname.<platform>`,
    or a configured `SCALIX_EDGE_IP`). On success, marks the domain active. This is
    the industry-standard \"does it point at us\" check (Vercel/Netlify/Render).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VerifyDomainResponse
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | VerifyDomainResponse]:
    r"""Verify a custom domain.

     Confirms — via a standard public DNS lookup, no provider credentials — that the
    customer's domain points at our edge (its A records match `cname.<platform>`,
    or a configured `SCALIX_EDGE_IP`). On success, marks the domain active. This is
    the industry-standard \"does it point at us\" check (Vercel/Netlify/Render).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | VerifyDomainResponse]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | VerifyDomainResponse | None:
    r"""Verify a custom domain.

     Confirms — via a standard public DNS lookup, no provider credentials — that the
    customer's domain points at our edge (its A records match `cname.<platform>`,
    or a configured `SCALIX_EDGE_IP`). On success, marks the domain active. This is
    the industry-standard \"does it point at us\" check (Vercel/Netlify/Render).

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | VerifyDomainResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
