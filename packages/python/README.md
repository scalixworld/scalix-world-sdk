# Scalix World SDK — Python

Python client for the Scalix World API. Provides async access to research, image generation, audio transcription, and text-to-speech.

## Installation

```bash
pip install scalix
```

## Quick Start

```python
from scalix import ScalixClient

scalix = ScalixClient(api_key="sk_scalix_...")

# Web search
results = await scalix.research.search("quantum computing")

# Standard research
answer = await scalix.research.research("explain quantum entanglement")

# Deep research
deep = await scalix.research.deep("compare fusion reactor designs")

# Image generation
image = await scalix.images.generate("A sunset over mountains")

# Async image generation (queue-based)
job = await scalix.images.generate_async("A futuristic city")
status = await scalix.images.get_job(job["jobId"])
result = await scalix.images.get_job_result(job["jobId"])

# List image models
models = await scalix.images.models()

# Audio transcription
with open("audio.mp3", "rb") as f:
    transcript = await scalix.audio.transcribe(f)

# Text-to-speech
audio = await scalix.audio.speak("Hello world", voice="af_heart")

# List available voices and languages
voices = await scalix.audio.voices()
languages = await scalix.audio.languages()
```

## Configuration

```python
import scalix

scalix.configure(
    api_key="sk_scalix_...",           # Required for cloud mode
    base_url="https://api.scalix.world",  # Default
    default_model="scalix-world-ai",
)
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SCALIX_API_KEY` | Scalix API key (enables cloud mode) |
| `SCALIX_BASE_URL` | Override API base URL (default: `https://api.scalix.world`) |
| `SCALIX_PROJECT_ID` | Project identifier |
| `OPENAI_API_KEY` | OpenAI key for local/BYOK mode |
| `ANTHROPIC_API_KEY` | Anthropic key for local/BYOK mode |
| `GOOGLE_API_KEY` | Google AI key for local/BYOK mode |
| `OLLAMA_HOST` | Ollama endpoint for local inference |

## API Endpoints

All requests go to `https://api.scalix.world` (override with `base_url` config or `SCALIX_BASE_URL` env var).

### Research

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/research/search` | `scalix.research.search(query)` |
| POST | `/v1/research` | `scalix.research.research(query)` |
| POST | `/v1/research/deep` | `scalix.research.deep(query)` |

### Images

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/images/generate` | `scalix.images.generate(prompt)` |
| POST | `/v1/images/generate/queue` | `scalix.images.generate_async(prompt)` |
| GET | `/v1/images/jobs/{jobId}` | `scalix.images.get_job(job_id)` |
| GET | `/v1/images/jobs/{jobId}/result` | `scalix.images.get_job_result(job_id)` |
| GET | `/v1/images/models` | `scalix.images.models()` |

### Audio

| Method | Endpoint | SDK Method |
|--------|----------|------------|
| POST | `/v1/audio/transcribe` | `scalix.audio.transcribe(file)` (multipart) |
| POST | `/v1/audio/speak/kokoro` | `scalix.audio.speak(text)` |
| GET | `/v1/audio/kokoro/voices` | `scalix.audio.voices()` |
| GET | `/v1/audio/kokoro/languages` | `scalix.audio.languages()` |

### Planned Services

The following services are available in the TypeScript SDK and will be added to the Python SDK:

- **Chat** — `POST /v1/chat/completions`, `GET /v1/models`
- **Text** — `POST /v1/text/sentiment`, `POST /v1/text/summarize`, `POST /v1/text/translate`
- **RAG** — `POST /v1/rag/upload`, `POST /v1/rag/query`, `GET /v1/rag/documents`, `DELETE /v1/rag/documents/{docId}`
- **DocGen** — `POST /v1/docgen/create`, `POST /v1/docgen/preview`, `GET /v1/docgen/formats`, `GET /v1/docgen/templates`, `GET /v1/docgen/history`, `GET /v1/docgen/download/{docId}`, `POST /v1/docgen/revise`, `GET /v1/docgen/versions/{docId}`
- **Storage** — `POST /v1/storage/upload-url`
- **ScalixDB** — `/api/scalixdb/databases/*`

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
