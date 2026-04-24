"""RAG service — document upload, query, and management."""

from __future__ import annotations

from typing import Any, BinaryIO

from scalix.services.base import BaseService


class RAGService(BaseService):
    async def upload(
        self, file: BinaryIO, *, filename: str | None = None
    ) -> dict[str, Any]:
        files = {"file": (filename, file) if filename else file}
        return await self._request_multipart("/v1/rag/upload", files=files)

    async def query(
        self,
        query: str,
        *,
        doc_ids: list[str] | None = None,
        top_k: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query}
        if doc_ids:
            body["doc_ids"] = doc_ids
        if top_k:
            body["top_k"] = top_k
        return await self._request("POST", "/v1/rag/query", json=body)

    async def documents(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/rag/documents")

    async def delete_document(self, doc_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"/v1/rag/documents/{doc_id}")
