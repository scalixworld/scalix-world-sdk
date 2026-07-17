from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.env_var import EnvVar
from ...models.error_response import ErrorResponse
from ...models.set_env_body import SetEnvBody
from ...types import Response


def _get_kwargs(
    *,
    body: SetEnvBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/env",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EnvVar | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = EnvVar.from_dict(response.json())

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
) -> Response[EnvVar | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SetEnvBody,
) -> Response[EnvVar | ErrorResponse]:
    """Set an environment variable.

     Creates or updates a single project-level environment variable.

    Args:
        body (SetEnvBody): Request body for `POST /v1/env` — a single project environment
            variable.
            Fields are read by serde + utoipa; the 501-stub handlers ignore the body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvVar | ErrorResponse]
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
    body: SetEnvBody,
) -> EnvVar | ErrorResponse | None:
    """Set an environment variable.

     Creates or updates a single project-level environment variable.

    Args:
        body (SetEnvBody): Request body for `POST /v1/env` — a single project environment
            variable.
            Fields are read by serde + utoipa; the 501-stub handlers ignore the body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvVar | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SetEnvBody,
) -> Response[EnvVar | ErrorResponse]:
    """Set an environment variable.

     Creates or updates a single project-level environment variable.

    Args:
        body (SetEnvBody): Request body for `POST /v1/env` — a single project environment
            variable.
            Fields are read by serde + utoipa; the 501-stub handlers ignore the body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvVar | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SetEnvBody,
) -> EnvVar | ErrorResponse | None:
    """Set an environment variable.

     Creates or updates a single project-level environment variable.

    Args:
        body (SetEnvBody): Request body for `POST /v1/env` — a single project environment
            variable.
            Fields are read by serde + utoipa; the 501-stub handlers ignore the body.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvVar | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
