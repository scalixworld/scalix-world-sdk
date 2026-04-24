# Scalix SDK — TypeScript

TypeScript client for the Scalix API. Provides typed access to chat, research, audio, text, RAG, document generation, database, storage, and account management.

## Installation

```bash
npm install @scalix-world/sdk
```

## Quick Start

```typescript
import { ScalixClient } from '@scalix-world/sdk';

const scalix = new ScalixClient({ apiKey: 'sk_scalix_...' });

// Chat completion (OpenAI-compatible)
const reply = await scalix.chat.complete({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Hello!' }],
});

// Streaming chat
for await (const chunk of scalix.chat.stream({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Tell me a story' }],
})) {
  process.stdout.write(chunk);
}

// Web search
const results = await scalix.research.search('quantum computing');

// Audio transcription
const transcript = await scalix.audio.transcribe(audioBlob);

// Text-to-speech
const audio = await scalix.audio.speak('Hello world');

// Text utilities
const sentiment = await scalix.text.sentiment('I love this product!');
const summary = await scalix.text.summarize(longArticle);
const translated = await scalix.text.translate('Hello', 'es');

// RAG — upload and query documents
const doc = await scalix.rag.upload(pdfBlob, { filename: 'report.pdf' });
const hits = await scalix.rag.query('revenue growth');

// Document generation
const report = await scalix.docgen.create({ prompt: 'Q1 report', format: 'pdf' });

// ScalixDB
const dbs = await scalix.database.list();
const db = await scalix.database.create({ name: 'my-app-db' });
const result = await scalix.database.query(db.database.id, 'SELECT * FROM users');

// Storage — presigned upload URL
const { uploadUrl } = await scalix.storage.getUploadUrl('application/pdf');

// Account — manage API keys
const keys = await scalix.account.listApiKeys();
const newKey = await scalix.account.createApiKey({ name: 'production-key' });

// Usage tracking
const usage = await scalix.account.usage({ startDate: '2026-04-01' });
```

## Configuration

```typescript
import { configure } from '@scalix-world/sdk';

configure({
  apiKey: 'sk_scalix_...',      // Required for cloud mode
  baseUrl: 'https://api.scalix.world', // Default
  defaultModel: 'scalix-world-ai',
});
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SCALIX_API_KEY` | Scalix API key (enables cloud mode) |
| `SCALIX_BASE_URL` | Override API base URL (default: `https://api.scalix.world`) |
| `SCALIX_PROJECT_ID` | Project identifier |

## API Endpoints

All requests go to `https://api.scalix.world` (override with `baseUrl` config or `SCALIX_BASE_URL` env var).

### Chat

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/chat/completions` | `scalix.chat.complete(options)` |
| POST | `/v1/chat/completions` | `scalix.chat.stream(options)` (streaming) |
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
| POST | `/v1/audio/transcribe` | `scalix.audio.transcribe(file)` (multipart) |
| POST | `/v1/audio/speak/kokoro` | `scalix.audio.speak(text)` |
| GET | `/v1/audio/kokoro/voices` | `scalix.audio.voices()` |
| GET | `/v1/audio/kokoro/languages` | `scalix.audio.languages()` |

### Text

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/text/sentiment` | `scalix.text.sentiment(text)` |
| POST | `/v1/text/summarize` | `scalix.text.summarize(text)` |
| POST | `/v1/text/translate` | `scalix.text.translate(text, targetLang)` |

### RAG

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/rag/upload` | `scalix.rag.upload(file)` (multipart) |
| POST | `/v1/rag/query` | `scalix.rag.query(query)` |
| GET | `/v1/rag/documents` | `scalix.rag.documents()` |
| DELETE | `/v1/rag/documents/{docId}` | `scalix.rag.deleteDocument(docId)` |

### Document Generation

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/docgen/create` | `scalix.docgen.create(options)` |
| POST | `/v1/docgen/preview` | `scalix.docgen.preview(options)` |
| GET | `/v1/docgen/formats` | `scalix.docgen.formats()` |
| GET | `/v1/docgen/templates` | `scalix.docgen.templates()` |
| GET | `/v1/docgen/history` | `scalix.docgen.history()` |
| GET | `/v1/docgen/download/{docId}` | `scalix.docgen.download(docId)` |
| POST | `/v1/docgen/revise` | `scalix.docgen.revise(docId, prompt)` |
| GET | `/v1/docgen/versions/{docId}` | `scalix.docgen.versions(docId)` |

### Storage

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/storage/upload-url` | `scalix.storage.getUploadUrl(mimeType)` |

### ScalixDB

All ScalixDB endpoints use the `/api/scalixdb/databases/*` path prefix.

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| GET | `/api/scalixdb/databases` | `scalix.database.list()` |
| POST | `/api/scalixdb/databases` | `scalix.database.create(options)` |
| GET | `/api/scalixdb/databases/{id}` | `scalix.database.get(id)` |
| PATCH | `/api/scalixdb/databases/{id}` | `scalix.database.update(id, updates)` |
| DELETE | `/api/scalixdb/databases/{id}` | `scalix.database.delete(id)` |
| POST | `/api/scalixdb/databases/{id}/query` | `scalix.database.query(id, sql)` |
| GET | `/api/scalixdb/databases/{id}/tables` | `scalix.database.listTables(id)` |
| GET | `/api/scalixdb/databases/{id}/metrics` | `scalix.database.getMetrics(id)` |
| GET | `/api/scalixdb/databases/{id}/connection` | `scalix.database.getConnection(id)` |
| GET | `/api/scalixdb/databases/{id}/branches` | `scalix.database.listBranches(id)` |
| GET | `/api/scalixdb/databases/{id}/backups` | `scalix.database.listBackups(id)` |

### Account

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| GET | `/health` | `scalix.account.health()` |
| GET | `/api/dashboard/api-keys` | `scalix.account.listApiKeys()` |
| POST | `/api/dashboard/api-keys` | `scalix.account.createApiKey({ name })` |
| DELETE | `/api/dashboard/api-keys/{id}` | `scalix.account.deleteApiKey(keyId)` |
| GET | `/api/billing/usage` | `scalix.account.usage()` |

## Error Handling

```typescript
import { ScalixClient } from '@scalix-world/sdk';

const scalix = new ScalixClient({ apiKey: 'sk_scalix_...' });

try {
  const result = await scalix.chat.complete({
    model: 'scalix-world-ai',
    messages: [{ role: 'user', content: 'Hello!' }],
  });
} catch (error) {
  if (error.status === 401) {
    console.error('Invalid API key');
  } else if (error.status === 429) {
    console.error('Rate limited — slow down');
  } else if (error.status === 402) {
    console.error('Usage limit reached — upgrade your plan');
  } else {
    console.error('API error:', error.message);
  }
}
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-advanced` | Most capable model — deep reasoning | Complex analysis, coding, agents |

## License

See [LICENSE](../../LICENSE) for details.
