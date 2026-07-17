from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_rule import CustomRule
from ...models.custom_rule_request import CustomRuleRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CustomRuleRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/shield/custom",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CustomRule | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CustomRule.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CustomRule | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CustomRuleRequest,
) -> Response[CustomRule | ErrorResponse]:
    """Create a custom Shield rule.

     Adds a customer-defined crawler rule matched by User-Agent substring, with
    its own access policy. Requires the Pro plan or higher.

    Args:
        body (CustomRuleRequest): Request body for `POST /v1/shield/custom` — a customer-defined
            UA rule.
            The `CrawlerPolicy` fields (`action`, `rate_limit_per_min`) are flattened
            into the top level alongside `name` and `ua_pattern`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomRule | ErrorResponse]
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
    body: CustomRuleRequest,
) -> CustomRule | ErrorResponse | None:
    """Create a custom Shield rule.

     Adds a customer-defined crawler rule matched by User-Agent substring, with
    its own access policy. Requires the Pro plan or higher.

    Args:
        body (CustomRuleRequest): Request body for `POST /v1/shield/custom` — a customer-defined
            UA rule.
            The `CrawlerPolicy` fields (`action`, `rate_limit_per_min`) are flattened
            into the top level alongside `name` and `ua_pattern`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomRule | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CustomRuleRequest,
) -> Response[CustomRule | ErrorResponse]:
    """Create a custom Shield rule.

     Adds a customer-defined crawler rule matched by User-Agent substring, with
    its own access policy. Requires the Pro plan or higher.

    Args:
        body (CustomRuleRequest): Request body for `POST /v1/shield/custom` — a customer-defined
            UA rule.
            The `CrawlerPolicy` fields (`action`, `rate_limit_per_min`) are flattened
            into the top level alongside `name` and `ua_pattern`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomRule | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CustomRuleRequest,
) -> CustomRule | ErrorResponse | None:
    """Create a custom Shield rule.

     Adds a customer-defined crawler rule matched by User-Agent substring, with
    its own access policy. Requires the Pro plan or higher.

    Args:
        body (CustomRuleRequest): Request body for `POST /v1/shield/custom` — a customer-defined
            UA rule.
            The `CrawlerPolicy` fields (`action`, `rate_limit_per_min`) are flattened
            into the top level alongside `name` and `ua_pattern`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomRule | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
