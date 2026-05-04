# Scalix SDK — Python

One SDK, one API key. `scalix.completions` gives you full OpenAI-compatible chat (tools, vision, streaming). The rest of the SDK gives you Research, RAG, DocGen, Database, Audio, Images — services that only Scalix has.

## Installation

```bash
pip install scalix openai
```

## Quick Start

```python
from scalix import Scalix

scalix = Scalix("sk_scalix_...")

# Chat completions — full OpenAI-compatible (tools, vision, streaming)
response = scalix.completions.create(
    model="scalix-world-ai",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Streaming
stream = scalix.completions.create(
    model="scalix-world-ai",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

# Tool calling
response = scalix.completions.create(
    model="scalix-world-ai",
    messages=[{"role": "user", "content": "What is the weather?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        },
    }],
)

# Vision
response = scalix.completions.create(
    model="scalix-world-ai",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is in this image?"},
            {"type": "image_url", "image_url": {"url": "https://..."}},
        ],
    }],
)
```

## Platform Services

These are Scalix-only services — no other SDK can reach them. All platform methods are async.

```python
# Research — web search and deep research
results = await scalix.research.search("quantum computing")
report = await scalix.research.deep("AI trends 2026")

# Audio — transcription and text-to-speech
with open("audio.mp3", "rb") as f:
    transcript = await scalix.audio.transcribe(f)
audio = await scalix.audio.speak("Hello world", voice="af_heart")

# Images — generation with sync and async modes
image = await scalix.images.generate("A sunset over mountains")
job = await scalix.images.generate_async("A detailed cityscape")

# Text — sentiment, summarization, translation
sentiment = await scalix.text.sentiment("I love this product!")
summary = await scalix.text.summarize(long_article)
translated = await scalix.text.translate("Hello", target_language="es")

# RAG — upload and query documents
doc = await scalix.rag.upload(pdf_file, filename="report.pdf")
answer = await scalix.rag.query("revenue growth")

# Document generation — PDF, DOCX, reports
pdf = await scalix.docgen.create(prompt="Q1 report", format="pdf")

# ScalixDB — managed databases
dbs = await scalix.database.list_databases()
result = await scalix.database.query(db_id, "SELECT * FROM users")

# Storage — presigned upload URLs
url = await scalix.storage.get_upload_url("application/pdf")

# Account — API keys and usage
keys = await scalix.account.list_api_keys()
usage = await scalix.account.usage(start_date="2026-04-01")

# Models — list available models with Scalix-specific fields
models = await scalix.models.list()
# Each model includes: context_window, max_output_tokens, plan_required, description
```

## Configuration

```python
from scalix import Scalix

scalix = Scalix(
    "sk_scalix_...",
    base_url="https://api.scalix.world",  # default
)

# For advanced OpenAI SDK usage (embeddings, raw access, etc.)
embedding = scalix.openai.embeddings.create(
    model="text-embedding-ada-002",
    input="Hello world",
)
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-world-advanced` | Most capable — deep reasoning | Complex analysis, coding, agents |

## Error Handling

```python
from scalix import Scalix, ScalixError, AuthenticationError

scalix = Scalix("sk_scalix_...")

try:
    # Chat errors come from the OpenAI SDK
    scalix.completions.create(...)
except openai.APIError:
    ...

try:
    # Platform service errors use Scalix error classes
    await scalix.research.search("...")
except AuthenticationError:
    print("Invalid API key")
except ScalixError as e:
    print(f"API error: {e}")
```

## Migration from v1

```python
# v1
from scalix import ScalixClient
scalix = ScalixClient(api_key="...")
await scalix.chat.complete(messages=[...])
async for chunk in scalix.chat.stream(messages=[...]):
    ...
await scalix.chat.models()

# v2
from scalix import Scalix
scalix = Scalix("sk_scalix_...")
scalix.completions.create(model="...", messages=[...])
scalix.completions.create(model="...", messages=[...], stream=True)
await scalix.models.list()

# All platform services (research, rag, database, etc.) are unchanged.
```

## Requirements

- Python >= 3.10
- openai >= 1.50.0
- httpx >= 0.25.0
- pydantic >= 2.5.0

## License

MIT
