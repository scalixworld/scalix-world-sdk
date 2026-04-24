# Scalix SDK

**One SDK for chat, research, audio, images, text, RAG, documents, databases, and more.**

The Scalix SDK gives developers typed access to the full [Scalix API](https://api.scalix.world). Available in Python and TypeScript.

## Quick Start

### Python

```bash
pip install scalix
```

```python
from scalix import ScalixClient

scalix = ScalixClient(api_key="sk_scalix_...")

# Chat completion (OpenAI-compatible)
result = await scalix.chat.complete(
    messages=[{"role": "user", "content": "Hello!"}],
    model="scalix-world-ai",
)

# Streaming
async for chunk in scalix.chat.stream(
    messages=[{"role": "user", "content": "Tell me a story"}],
):
    print(chunk, end="")

# Web search
results = await scalix.research.search("quantum computing")

# Text-to-speech
audio = await scalix.audio.speak("Hello world")

# Image generation
image = await scalix.images.generate("A sunset over mountains")

# Text utilities
sentiment = await scalix.text.sentiment("I love this product!")

# Account management
keys = await scalix.account.list_api_keys()
usage = await scalix.account.usage()
```

### TypeScript

```bash
npm install @scalix-world/sdk
```

```typescript
import { ScalixClient } from '@scalix-world/sdk';

const scalix = new ScalixClient({ apiKey: 'sk_scalix_...' });

// Chat completion (OpenAI-compatible)
const reply = await scalix.chat.complete({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Hello!' }],
});

// Streaming
for await (const chunk of scalix.chat.stream({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Tell me a story' }],
})) {
  process.stdout.write(chunk);
}

// Web search
const results = await scalix.research.search('quantum computing');

// Text-to-speech
const audio = await scalix.audio.speak('Hello world');

// Image generation
const image = await scalix.images.generate('A sunset over mountains');

// Account management
const keys = await scalix.account.listApiKeys();
const usage = await scalix.account.usage();
```

## Services

| Service | Description | Example |
|---------|-------------|---------|
| **Chat** | OpenAI-compatible completions + streaming | `scalix.chat.complete(...)` |
| **Research** | Web search, standard + deep research | `scalix.research.search(query)` |
| **Audio** | Text-to-speech, transcription, voice list | `scalix.audio.speak(text)` |
| **Images** | Image generation, async queuing | `scalix.images.generate(prompt)` |
| **Text** | Sentiment, summarize, translate | `scalix.text.sentiment(text)` |
| **RAG** | Upload documents, semantic query | `scalix.rag.query(question)` |
| **DocGen** | Generate PDFs, DOCX, XLSX from prompts | `scalix.docgen.create(prompt, format)` |
| **Database** | Managed Postgres (ScalixDB) | `scalix.database.query(id, sql)` |
| **Storage** | Presigned upload URLs | `scalix.storage.get_upload_url(mime)` |
| **Account** | API keys, usage tracking, health | `scalix.account.usage()` |

## API Endpoints

All requests go to `https://api.scalix.world`.

| Category | Method | Endpoint | Description |
|----------|--------|----------|-------------|
| Chat | POST | `/v1/chat/completions` | Chat completions (OpenAI-compatible) |
| Chat | GET | `/v1/models` | List available models |
| Research | POST | `/v1/research/search` | Web search |
| Research | POST | `/v1/research` | Standard research |
| Research | POST | `/v1/research/deep` | Deep research |
| Audio | POST | `/v1/audio/transcribe` | Speech-to-text (multipart) |
| Audio | POST | `/v1/audio/speak/kokoro` | Text-to-speech |
| Audio | GET | `/v1/audio/kokoro/voices` | Voice list |
| Audio | GET | `/v1/audio/kokoro/languages` | Supported languages |
| Images | POST | `/v1/images/generate` | Generate image |
| Images | POST | `/v1/images/generate/queue` | Queue async generation |
| Images | GET | `/v1/images/jobs/{jobId}` | Check job status |
| Images | GET | `/v1/images/jobs/{jobId}/result` | Get job result |
| Images | GET | `/v1/images/models` | List image models |
| Text | POST | `/v1/text/sentiment` | Sentiment analysis |
| Text | POST | `/v1/text/summarize` | Summarize text |
| Text | POST | `/v1/text/translate` | Translate text |
| RAG | POST | `/v1/rag/upload` | Upload document (multipart) |
| RAG | POST | `/v1/rag/query` | Query documents |
| RAG | GET | `/v1/rag/documents` | List documents |
| RAG | DELETE | `/v1/rag/documents/{docId}` | Delete document |
| DocGen | POST | `/v1/docgen/create` | Create document |
| DocGen | POST | `/v1/docgen/preview` | Preview document |
| DocGen | GET | `/v1/docgen/formats` | Supported formats |
| DocGen | GET | `/v1/docgen/templates` | Templates |
| DocGen | GET | `/v1/docgen/history` | Generation history |
| DocGen | POST | `/v1/docgen/revise` | Revise document |
| DocGen | GET | `/v1/docgen/versions/{docId}` | Document versions |
| Storage | POST | `/v1/storage/upload-url` | Presigned upload URL |
| ScalixDB | GET | `/api/scalixdb/databases` | List databases |
| ScalixDB | POST | `/api/scalixdb/databases` | Create database |
| ScalixDB | POST | `/api/scalixdb/databases/{id}/query` | Run SQL query |
| Account | GET | `/health` | Service health check |
| Account | GET | `/api/dashboard/api-keys` | List your API keys |
| Account | POST | `/api/dashboard/api-keys` | Create API key |
| Account | DELETE | `/api/dashboard/api-keys/{id}` | Delete API key |
| Account | GET | `/api/billing/usage` | Usage & billing breakdown |

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-advanced` | Most capable model — deep reasoning | Complex analysis, coding, agents |

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SCALIX_API_KEY` | Scalix API key |
| `SCALIX_BASE_URL` | Override API base URL |

## Packages

| Package | Registry | Install |
|---------|----------|---------|
| `scalix` | PyPI | `pip install scalix` |
| `@scalix-world/sdk` | npm | `npm install @scalix-world/sdk` |

## License

MIT
