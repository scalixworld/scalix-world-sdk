from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_subject_request import DataSubjectRequest
from ...models.error_response import ErrorResponse
from ...models.update_gdpr_status_body import UpdateGdprStatusBody
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: UpdateGdprStatusBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/compliance/gdpr/requests/{id}/status".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DataSubjectRequest | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DataSubjectRequest.from_dict(response.json())

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
) -> Response[DataSubjectRequest | ErrorResponse]:
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
    body: UpdateGdprStatusBody,
) -> Response[DataSubjectRequest | ErrorResponse]:
    """Advance a GDPR data-subject request through its lifecycle.

     SEC-1: the DSR flow was intake-only — requests sat `pending` forever with no
    way to fulfill them, while the compliance status implied a working workflow.
    A data-protection officer (compliance:write) now moves each request through
    pending → in_progress → completed/rejected; terminal states stamp
    `completed_at`, giving an auditable fulfillment record within the GDPR Art.
    12(3) one-month window. Tenant-scoped.

    Args:
        id (str):
        body (UpdateGdprStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSubjectRequest | ErrorResponse]
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
    body: UpdateGdprStatusBody,
) -> DataSubjectRequest | ErrorResponse | None:
    """Advance a GDPR data-subject request through its lifecycle.

     SEC-1: the DSR flow was intake-only — requests sat `pending` forever with no
    way to fulfill them, while the compliance status implied a working workflow.
    A data-protection officer (compliance:write) now moves each request through
    pending → in_progress → completed/rejected; terminal states stamp
    `completed_at`, giving an auditable fulfillment record within the GDPR Art.
    12(3) one-month window. Tenant-scoped.

    Args:
        id (str):
        body (UpdateGdprStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSubjectRequest | ErrorResponse
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
    body: UpdateGdprStatusBody,
) -> Response[DataSubjectRequest | ErrorResponse]:
    """Advance a GDPR data-subject request through its lifecycle.

     SEC-1: the DSR flow was intake-only — requests sat `pending` forever with no
    way to fulfill them, while the compliance status implied a working workflow.
    A data-protection officer (compliance:write) now moves each request through
    pending → in_progress → completed/rejected; terminal states stamp
    `completed_at`, giving an auditable fulfillment record within the GDPR Art.
    12(3) one-month window. Tenant-scoped.

    Args:
        id (str):
        body (UpdateGdprStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSubjectRequest | ErrorResponse]
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
    body: UpdateGdprStatusBody,
) -> DataSubjectRequest | ErrorResponse | None:
    """Advance a GDPR data-subject request through its lifecycle.

     SEC-1: the DSR flow was intake-only — requests sat `pending` forever with no
    way to fulfill them, while the compliance status implied a working workflow.
    A data-protection officer (compliance:write) now moves each request through
    pending → in_progress → completed/rejected; terminal states stamp
    `completed_at`, giving an auditable fulfillment record within the GDPR Art.
    12(3) one-month window. Tenant-scoped.

    Args:
        id (str):
        body (UpdateGdprStatusBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSubjectRequest | ErrorResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
