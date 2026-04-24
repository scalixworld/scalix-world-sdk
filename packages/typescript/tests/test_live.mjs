/**
 * Live integration tests for Scalix World SDK (TypeScript).
 * Tests against real api.scalix.world infrastructure.
 */

const API_KEY = "sk_scalix_c87da0be98241b19674180fd724cfa0600d02b759a5ef16848a8c08763419b93";
const BASE_URL = "https://api.scalix.world";

let passed = 0;
let failed = 0;
let total = 0;

function report(name, success, detail = "") {
  total++;
  if (success) {
    passed++;
    console.log(`  ✅ ${name}`);
  } else {
    failed++;
    console.log(`  ❌ ${name}: ${detail}`);
  }
}

async function apiCall(method, path, body = null) {
  const url = `${BASE_URL}${path}`;
  const opts = {
    method,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
  };
  if (body) opts.body = JSON.stringify(body);
  const resp = await fetch(url, opts);
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
  return resp.json();
}

// Chat
async function testChatComplete() {
  try {
    const result = await apiCall("POST", "/v1/chat/completions", {
      model: "scalix-world-ai",
      messages: [{ role: "user", content: "Say 'hello' and nothing else." }],
      max_tokens: 20,
      temperature: 0.1,
    });
    const content = result.choices?.[0]?.message?.content || "";
    report(`chat.complete (response: '${content.slice(0, 40)}')`, !!content);
  } catch (e) {
    report("chat.complete", false, e.message);
  }
}

async function testChatModels() {
  try {
    const result = await apiCall("GET", "/v1/models");
    const models = result.data || [];
    report(`chat.models (got ${models.length} models)`, models.length > 0);
  } catch (e) {
    report("chat.models", false, e.message);
  }
}

// Research
async function testResearchSearch() {
  try {
    const result = await apiCall("POST", "/v1/research/search?query=quantum+computing");
    report(`research.search (keys: ${Object.keys(result).slice(0, 3)})`, !!result);
  } catch (e) {
    report("research.search", false, e.message);
  }
}

// Text
async function testTextSentiment() {
  try {
    const result = await apiCall("POST", "/v1/text/sentiment", { text: "I love this product!" });
    report(`text.sentiment (${result.sentiment || result.label || "?"})`, !!result);
  } catch (e) {
    report("text.sentiment", false, e.message);
  }
}

async function testTextSummarize() {
  try {
    const result = await apiCall("POST", "/v1/text/summarize", {
      text: "AI has transformed many industries. Machine learning can process language, generate images, and write code.",
    });
    report(`text.summarize (keys: ${Object.keys(result).slice(0, 3)})`, !!result);
  } catch (e) {
    report("text.summarize", false, e.message);
  }
}

async function testTextTranslate() {
  try {
    const result = await apiCall("POST", "/v1/text/translate", {
      text: "Hello, how are you?",
      target_language: "es",
    });
    report(`text.translate (${JSON.stringify(result).slice(0, 60)})`, !!result);
  } catch (e) {
    report("text.translate", false, e.message);
  }
}

// Audio
async function testAudioVoices() {
  try {
    const result = await apiCall("GET", "/v1/audio/kokoro/voices");
    report(`audio.voices (keys: ${Object.keys(result).slice(0, 3)})`, !!result);
  } catch (e) {
    report("audio.voices", false, e.message);
  }
}

// DocGen
async function testDocGenFormats() {
  try {
    const result = await apiCall("GET", "/v1/docgen/formats");
    report(`docgen.formats (type: ${Array.isArray(result) ? "array" : typeof result})`, !!result);
  } catch (e) {
    report("docgen.formats", false, e.message);
  }
}

async function testDocGenTemplates() {
  try {
    const result = await apiCall("GET", "/v1/docgen/templates");
    report(`docgen.templates (type: ${Array.isArray(result) ? "array" : typeof result})`, !!result);
  } catch (e) {
    report("docgen.templates", false, e.message);
  }
}

// Database
async function testDatabaseList() {
  try {
    const result = await apiCall("GET", "/api/scalixdb/databases");
    report(`database.list (type: ${typeof result})`, true);
  } catch (e) {
    report("database.list", false, e.message);
  }
}

// RAG
async function testRagDocuments() {
  try {
    const result = await apiCall("GET", "/v1/rag/documents");
    report(`rag.documents (type: ${typeof result})`, true);
  } catch (e) {
    report("rag.documents", false, e.message);
  }
}

// Account
async function testAdminHealth() {
  try {
    const result = await apiCall("GET", "/health");
    report(`account.health (keys: ${Object.keys(result).slice(0, 3)})`, !!result);
  } catch (e) {
    report("account.health", false, e.message);
  }
}

async function testAdminListApiKeys() {
  try {
    const result = await apiCall("GET", "/api/dashboard/api-keys");
    report(`account.listApiKeys (type: ${typeof result})`, !!result);
  } catch (e) {
    report("account.listApiKeys", false, e.message);
  }
}

async function testAdminUsage() {
  try {
    const result = await apiCall("GET", "/api/billing/usage");
    report(`account.usage (type: ${typeof result})`, !!result);
  } catch (e) {
    report("account.usage", false, e.message);
  }
}

async function main() {
  console.log("\n" + "=".repeat(60));
  console.log("SCALIX WORLD SDK (TYPESCRIPT) — LIVE INTEGRATION TESTS");
  console.log(`Target: ${BASE_URL}`);
  console.log("=".repeat(60) + "\n");

  console.log("💬 Chat Service:");
  await testChatComplete();
  await testChatModels();

  console.log("\n🔍 Research Service:");
  await testResearchSearch();

  console.log("\n📝 Text Service:");
  await testTextSentiment();
  await testTextSummarize();
  await testTextTranslate();

  console.log("\n🔊 Audio Service:");
  await testAudioVoices();

  console.log("\n📄 DocGen Service:");
  await testDocGenFormats();
  await testDocGenTemplates();

  console.log("\n🗄️  Database Service:");
  await testDatabaseList();

  console.log("\n📚 RAG Service:");
  await testRagDocuments();

  console.log("\n🔧 Account Service:");
  await testAdminHealth();
  await testAdminListApiKeys();
  await testAdminUsage();

  console.log("\n" + "=".repeat(60));
  console.log(`RESULTS: ${passed}/${total} passed, ${failed} failed`);
  if (failed === 0) {
    console.log("✅ ALL TESTS PASSED");
  } else {
    console.log(`❌ ${failed} TESTS FAILED`);
  }
  console.log("=".repeat(60) + "\n");

  process.exit(failed === 0 ? 0 : 1);
}

main();
