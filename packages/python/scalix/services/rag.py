"""RAG service — document upload and querying."""

from __future__ import annotations

from typing import Any, BinaryIO

from scalix.services.base import BaseService


class RAGService(BaseService):
    async def upload(
        self, file: BinaryIO, *, filename: str | None = None
    ) -> dict[str, Any]:
        files = {"file": (filename or "document", file)}
        return await self._request_multipart("/v1/rag/upload", files=files)

    async def query(
        self, query: str, *, doc_ids: list[str] | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query}
        if doc_ids:
            body["doc_ids"] = doc_ids
        return await self._request("POST", "/v1/rag/query", json=body)

    async def list_documents(self) -> dict[str, Any]:
        return await self._request("GET", "/v1/rag/documents")

    async def delete_document(self, doc_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"/v1/rag/documents/{doc_id}")
