# Scalix SDK — TypeScript

One SDK, one API key. `scalix.completions` gives you full OpenAI-compatible chat (tools, vision, streaming). The rest of the SDK gives you Research, RAG, DocGen, Audio, Images, Text — services that only Scalix has.

## Installation

```bash
npm install @scalix-world/sdk openai
```

## Quick Start

```typescript
import { Scalix } from '@scalix-world/sdk';

const scalix = new Scalix('sk_scalix_...');

// Chat completions — full OpenAI-compatible (tools, vision, streaming)
const response = await scalix.completions.create({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Hello!' }],
});

// Streaming
const stream = await scalix.completions.create({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}
```

## Platform Services

These are Scalix-only services — no other SDK can reach them.

### Research — web search and deep research

```typescript
const results = await scalix.research.search('quantum computing');
const report = await scalix.research.deep('AI trends 2026');
const answer = await scalix.research.research('What is GraphQL?');
```

### Text — sentiment, summarization, translation, grammar, autocomplete

```typescript
const sentiment = await scalix.text.sentiment('I love this product!');
const summary = await scalix.text.summarize(longArticle);
const translated = await scalix.text.translate('Hello', 'es');
const grammar = await scalix.text.grammar('Me and him goes to store');
const completion = await scalix.text.autocomplete('The quick brown');
```

### Audio — transcription and text-to-speech

```typescript
const transcript = await scalix.audio.transcribe(audioBlob);
const audio = await scalix.audio.speak('Hello world', { voice: 'af_heart' });
const voices = await scalix.audio.voices();
const languages = await scalix.audio.languages();
```

### Images — generation with sync and async modes

```typescript
const image = await scalix.images.generate('A sunset over mountains');
const job = await scalix.images.generateAsync('A detailed cityscape');
const status = await scalix.images.getJob(job.job_id);
const models = await scalix.images.models();
```

### Document Generation — PDF, DOCX, CSV, XLSX

```typescript
const doc = await scalix.docgen.create({ prompt: 'Q1 report', format: 'pdf' });
const history = await scalix.docgen.history();
const formats = await scalix.docgen.formats();
const templates = await scalix.docgen.templates();
await scalix.docgen.share(doc.doc_id, 'colleague@company.com');
```

### RAG — upload and query documents

```typescript
const doc = await scalix.rag.upload(pdfBlob, { filename: 'report.pdf' });
const answer = await scalix.rag.query('revenue growth');
const docs = await scalix.rag.documents();
await scalix.rag.deleteDocument(docId);
```

### Storage — presigned upload URLs

```typescript
const { uploadUrl } = await scalix.storage.getUploadUrl('application/pdf');
```

### Account — health, info, budget, usage

```typescript
const health = await scalix.account.health();
const info = await scalix.account.info();     // email, plan
const budget = await scalix.account.budget(); // credits remaining
const usage = await scalix.account.usage();   // usage stats
```

### Models — list available models

```typescript
const models = await scalix.models.list();
// Each model includes: id, context_window, max_output_tokens, plan_required
```

## Configuration

```typescript
const scalix = new Scalix('sk_scalix_...', {
  baseURL: 'https://api.scalix.world', // default
  maxRetries: 2,                        // auto-retry with exponential backoff
  timeout: 60000,                       // request timeout in ms
});
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-world-advanced` | Most capable — deep reasoning | Complex analysis, coding, agents |

Plus 12 more models — run `scalix.models.list()` to see all available for your plan.

## Error Handling

```typescript
import { Scalix, ScalixError, AuthenticationError, RateLimitError } from '@scalix-world/sdk';

try {
  await scalix.research.search('...');
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.error('Rate limited — SDK retries automatically');
  } else if (error instanceof ScalixError) {
    console.error('API error:', error.message);
  }
}
```

## License

MIT — see [LICENSE](./LICENSE) for details.
