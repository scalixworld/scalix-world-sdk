# Scalix SDK — TypeScript

One SDK, one API key. `scalix.completions` gives you full OpenAI-compatible chat (tools, vision, streaming). The rest of the SDK gives you Research, RAG, DocGen, Database, Audio, Images — services that only Scalix has.

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

// Tool calling
const toolResponse = await scalix.completions.create({
  model: 'scalix-world-ai',
  messages: [{ role: 'user', content: 'What is the weather?' }],
  tools: [{
    type: 'function',
    function: {
      name: 'get_weather',
      parameters: { type: 'object', properties: { city: { type: 'string' } } },
    },
  }],
});

// Vision
const visionResponse = await scalix.completions.create({
  model: 'scalix-world-ai',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What is in this image?' },
      { type: 'image_url', image_url: { url: 'https://...' } },
    ],
  }],
});
```

## Platform Services

These are Scalix-only services — no other SDK can reach them.

```typescript
// Research — web search and deep research
const results = await scalix.research.search('quantum computing');
const report = await scalix.research.deep('AI trends 2026');

// Audio — transcription and text-to-speech
const transcript = await scalix.audio.transcribe(audioBlob);
const audio = await scalix.audio.speak('Hello world');

// Images — generation with sync and async modes
const image = await scalix.images.generate('A sunset over mountains');
const job = await scalix.images.generateAsync('A detailed cityscape');

// Text — sentiment, summarization, translation
const sentiment = await scalix.text.sentiment('I love this product!');
const summary = await scalix.text.summarize(longArticle);
const translated = await scalix.text.translate('Hello', 'es');

// RAG — upload and query documents
const doc = await scalix.rag.upload(pdfBlob, { filename: 'report.pdf' });
const answer = await scalix.rag.query('revenue growth');

// Document generation — PDF, DOCX, reports
const pdf = await scalix.docgen.create({ prompt: 'Q1 report', format: 'pdf' });

// ScalixDB — managed databases
const dbs = await scalix.database.list();
const db = await scalix.database.create({ name: 'my-app-db' });
const result = await scalix.database.query(db.database.id, 'SELECT * FROM users');

// Storage — presigned upload URLs
const { uploadUrl } = await scalix.storage.getUploadUrl('application/pdf');

// Account — API keys and usage
const keys = await scalix.account.listApiKeys();
const usage = await scalix.account.usage({ startDate: '2026-04-01' });

// Models — list available models with Scalix-specific fields
const models = await scalix.models.list();
// Each model includes: context_window, max_output_tokens, plan_required, description
```

## Configuration

```typescript
import { Scalix } from '@scalix-world/sdk';

const scalix = new Scalix('sk_scalix_...', {
  baseURL: 'https://api.scalix.world', // default
});

// For advanced OpenAI SDK usage (embeddings, raw access, etc.)
const embedding = await scalix.openai.embeddings.create({
  model: 'text-embedding-ada-002',
  input: 'Hello world',
});
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `scalix-world-ai` | Default model — fast, balanced | General use, chat, quick tasks |
| `scalix-world-advanced` | Most capable — deep reasoning | Complex analysis, coding, agents |

## Error Handling

```typescript
import { Scalix, ScalixError, AuthenticationError } from '@scalix-world/sdk';

const scalix = new Scalix('sk_scalix_...');

try {
  // Chat errors come from the OpenAI SDK
  await scalix.completions.create({ ... });
} catch (error) {
  // OpenAI SDK errors for chat
}

try {
  // Platform service errors use Scalix error classes
  await scalix.research.search('...');
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Invalid API key');
  } else if (error instanceof ScalixError) {
    console.error('API error:', error.message);
  }
}
```

## Migration from v1

```typescript
// v1
import { ScalixClient } from '@scalix-world/sdk';
const scalix = new ScalixClient({ apiKey: '...' });
await scalix.chat.complete({ model: '...', messages: [...] });
await scalix.chat.stream({ ... });
await scalix.chat.models();

// v2
import { Scalix } from '@scalix-world/sdk';
const scalix = new Scalix('sk_scalix_...');
await scalix.completions.create({ model: '...', messages: [...] });
await scalix.completions.create({ model: '...', messages: [...], stream: true });
await scalix.models.list();

// All platform services (research, rag, database, etc.) are unchanged.
```

## License

See [LICENSE](../../LICENSE) for details.
