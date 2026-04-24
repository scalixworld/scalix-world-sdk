# Scalix SDK — Python

Python client for the Scalix API. Provides async access to chat, research, audio, text, RAG, document generation, database, storage, and account management.

## Installation

```bash
pip install scalix
```

## Quick Start

```python
from scalix import ScalixClient

scalix = ScalixClient(api_key="sk_scalix_...")

# Chat completion (OpenAI-compatible)
result = await scalix.chat.complete(
    messages=[{"role": "user", "content": "Hello!"}],
    model="scalix-world-ai",
)

# Streaming chat
async for chunk in scalix.chat.stream(
    messages=[{"role": "user", "content": "Tell me a story"}],
    model="scalix-world-ai",
):
    print(chunk, end="")

# Web search
results = await scalix.research.search("quantum computing")

# Deep research
deep = await scalix.research.deep("compare fusion reactor designs")

# Text-to-speech
audio = await scalix.audio.speak("Hello world", voice="af_heart")

# Audio transcription
with open("audio.mp3", "rb") as f:
    transcript = await scalix.audio.transcribe(f)

# Text utilities
sentiment = await scalix.text.sentiment("I love this product!")
summary = await scalix.text.summarize(long_article)
translated = await scalix.text.translate("Hello", target_language="es")

# RAG — upload and query documents
doc = await scalix.rag.upload(pdf_file, filename="report.pdf")
hits = await scalix.rag.query("revenue growth")

# Document generation
report = await scalix.docgen.create(prompt="Q1 report", format="pdf")

# ScalixDB
dbs = await scalix.database.list_databases()
result = await scalix.database.query(db_id, "SELECT * FROM users")

# Account — manage API keys
keys = await scalix.account.list_api_keys()
new_key = await scalix.account.create_api_key("production-key")

# Usage tracking
usage = await scalix.account.usage(start_date="2026-04-01")
```

## Configuration

```python
import scalix

scalix.configure(
    api_key="sk_scalix_...",              # Required
    base_url="https://api.scalix.world",  # Default
    default_model="scalix-world-ai",
)
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SCALIX_API_KEY` | Scalix API key |
| `SCALIX_BASE_URL` | Override API base URL (default: `https://api.scalix.world`) |

## API Endpoints

All requests go to `https://api.scalix.world`.

### Chat

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/chat/completions` | `scalix.chat.complete(messages)` |
| POST | `/v1/chat/completions` | `scalix.chat.stream(messages)` (streaming) |
| GET | `/v1/models` | `scalix.chat.models()` |

### Research

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/research/search` | `scalix.research.search(query)` |
| POST | `/v1/research` | `scalix.research.research(query)` |
| POST | `/v1/research/deep` | `scalix.research.deep(query)` |

### Audio

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/audio/transcribe` | `scalix.audio.transcribe(file)` |
| POST | `/v1/audio/speak/kokoro` | `scalix.audio.speak(text)` |
| GET | `/v1/audio/kokoro/voices` | `scalix.audio.voices()` |
| GET | `/v1/audio/kokoro/languages` | `scalix.audio.languages()` |

### Text

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/text/sentiment` | `scalix.text.sentiment(text)` |
| POST | `/v1/text/summarize` | `scalix.text.summarize(text)` |
| POST | `/v1/text/translate` | `scalix.text.translate(text, target_language)` |

### RAG

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/rag/upload` | `scalix.rag.upload(file)` |
| POST | `/v1/rag/query` | `scalix.rag.query(query)` |
| GET | `/v1/rag/documents` | `scalix.rag.documents()` |
| DELETE | `/v1/rag/documents/{docId}` | `scalix.rag.delete_document(doc_id)` |

### Document Generation

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/docgen/create` | `scalix.docgen.create(prompt, format)` |
| POST | `/v1/docgen/preview` | `scalix.docgen.preview(prompt)` |
| GET | `/v1/docgen/formats` | `scalix.docgen.formats()` |
| GET | `/v1/docgen/templates` | `scalix.docgen.templates()` |
| GET | `/v1/docgen/history` | `scalix.docgen.history()` |
| POST | `/v1/docgen/revise` | `scalix.docgen.revise(doc_id, prompt)` |
| GET | `/v1/docgen/versions/{docId}` | `scalix.docgen.versions(doc_id)` |

### Storage

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/storage/upload-url` | `scalix.storage.get_upload_url(mime_type)` |

### ScalixDB

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| GET | `/api/scalixdb/databases` | `scalix.database.list_databases()` |
| POST | `/api/scalixdb/databases` | `scalix.database.create_database(name)` |
| GET | `/api/scalixdb/databases/{id}` | `scalix.database.get_database(db_id)` |
| DELETE | `/api/scalixdb/databases/{id}` | `scalix.database.delete_database(db_id)` |
| POST | `/api/scalixdb/databases/{id}/query` | `scalix.database.query(db_id, sql)` |
| GET | `/api/scalixdb/databases/{id}/tables` | `scalix.database.tables(db_id)` |
| GET | `/api/scalixdb/databases/{id}/metrics` | `scalix.database.metrics(db_id)` |
| GET | `/api/scalixdb/databases/{id}/branches` | `scalix.database.list_branches(db_id)` |
| GET | `/api/scalixdb/databases/{id}/backups` | `scalix.database.list_backups(db_id)` |

### Account

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| GET | `/health` | `scalix.account.health()` |
| GET | `/api/dashboard/api-keys` | `scalix.account.list_api_keys()` |
| POST | `/api/dashboard/api-keys` | `scalix.account.create_api_key(name)` |
| DELETE | `/api/dashboard/api-keys/{id}` | `scalix.account.delete_api_key(key_id)` |
| GET | `/api/billing/usage` | `scalix.account.usage()` |

## Error Handling

```python
from scalix import ScalixClient
from httpx import HTTPStatusError

scalix = ScalixClient(api_key="sk_scalix_...")

try:
    result = await scalix.chat.complete(
        messages=[{"role": "user", "content": "Hello"}],
    )
except HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limited — slow down")
    elif e.response.status_code == 402:
        print("Usage limit reached — upgrade your plan")
    else:
        print(f"API error: {e.response.status_code}")
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-advanced` | Most capable model — deep reasoning | Complex analysis, coding, agents |

## Requirements

- Python >= 3.10
- httpx >= 0.25.0
- pydantic >= 2.5.0

## License

MIT
