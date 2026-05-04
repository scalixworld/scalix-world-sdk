# Scalix SDK — Python

One SDK, one API key. `scalix.completions` gives you full OpenAI-compatible chat (tools, vision, streaming). The rest of the SDK gives you Research, RAG, DocGen, Audio, Images, Text — services that only Scalix has.

## Installation

```bash
pip install scalix
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
```

## Platform Services

These are Scalix-only services — no other SDK can reach them. All platform methods are async.

### Research — web search and deep research

```python
results = await scalix.research.search("quantum computing")
report = await scalix.research.deep("AI trends 2026")
answer = await scalix.research.research("What is GraphQL?")
```

### Text — sentiment, summarization, translation, grammar, autocomplete

```python
sentiment = await scalix.text.sentiment("I love this product!")
summary = await scalix.text.summarize(long_article)
translated = await scalix.text.translate("Hello", "es")
grammar = await scalix.text.grammar("Me and him goes to store")
completion = await scalix.text.autocomplete("The quick brown")
```

### Audio — transcription and text-to-speech

```python
with open("audio.mp3", "rb") as f:
    transcript = await scalix.audio.transcribe(f)
audio = await scalix.audio.speak("Hello world", voice="af_heart")
voices = await scalix.audio.voices()
languages = await scalix.audio.languages()
```

### Images — generation with sync and async modes

```python
image = await scalix.images.generate("A sunset over mountains")
job = await scalix.images.generate_async("A detailed cityscape")
status = await scalix.images.get_job(job["job_id"])
models = await scalix.images.models()
```

### Document Generation — PDF, DOCX, CSV, XLSX

```python
doc = await scalix.docgen.create(prompt="Q1 report", format="pdf")
history = await scalix.docgen.history()
formats = await scalix.docgen.formats()
templates = await scalix.docgen.templates()
await scalix.docgen.share(doc["doc_id"], "colleague@company.com")
```

### RAG — upload and query documents

```python
doc = await scalix.rag.upload(pdf_file, filename="report.pdf")
answer = await scalix.rag.query("revenue growth")
docs = await scalix.rag.documents()
await scalix.rag.delete_document(doc_id)
```

### Storage — presigned upload URLs

```python
url = await scalix.storage.get_upload_url("application/pdf")
```

### Account — health, info, budget, usage

```python
health = await scalix.account.health()
info = await scalix.account.info()       # email, plan
budget = await scalix.account.budget()   # credits remaining
usage = await scalix.account.usage()     # usage stats
```

### Models — list available models

```python
models = await scalix.models.list()
# Each model includes: id, context_window, max_output_tokens, plan_required
```

## Configuration

```python
scalix = Scalix(
    "sk_scalix_...",
    base_url="https://api.scalix.world",  # default
    max_retries=2,                         # auto-retry with exponential backoff
    timeout=60.0,                          # request timeout in seconds
)
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-world-advanced` | Most capable — deep reasoning | Complex analysis, coding, agents |

Plus 12 more models — run `await scalix.models.list()` to see all available for your plan.

## Error Handling

```python
from scalix import Scalix, ScalixError, AuthenticationError, RateLimitError

try:
    await scalix.research.search("...")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limited — SDK retries automatically")
except ScalixError as e:
    print(f"API error: {e}")
```

## Requirements

- Python >= 3.10
- openai >= 1.50.0
- httpx >= 0.25.0
- pydantic >= 2.5.0

## License

MIT — see [LICENSE](./LICENSE) for details.
