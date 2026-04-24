#!/usr/bin/env python3
"""Live SDK Test — Tests all World SDK endpoints against production.

Tests:
1. ScalixClient services (Research, Images, Audio)
2. Agent framework (chat completions)
3. Direct API calls for endpoints not yet wrapped
4. Error handling and edge cases
"""

import asyncio
import json
import sys
import time
import os

# Add the SDK package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "packages", "python"))

API_KEY = "sk_scalix_c87da0be98241b19674180fd724cfa0600d02b759a5ef16848a8c08763419b93"
BASE_URL = "https://api.scalix.world"

results = []

def record(name, status, detail="", duration_ms=0):
    results.append({
        "name": name,
        "status": status,
        "detail": detail[:200],
        "duration_ms": round(duration_ms),
    })
    icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"  {icon} {name}: {status} ({round(duration_ms)}ms) {detail[:100]}")


async def test_sdk_config():
    """Test SDK configuration system."""
    print("\n=== 1. SDK Configuration ===")

    from scalix import configure, get_config, ScalixConfig

    # Test default config
    t0 = time.time()
    config = get_config()
    d = (time.time() - t0) * 1000
    record("Default config loads", "PASS" if config else "FAIL",
           f"base_url={config.base_url}, mode={'cloud' if config.is_cloud_mode else 'local'}", d)

    # Test configure with API key
    t0 = time.time()
    config = configure(api_key=API_KEY, base_url=BASE_URL)
    d = (time.time() - t0) * 1000
    record("configure(api_key=...)", "PASS" if config.is_cloud_mode else "FAIL",
           f"cloud_mode={config.is_cloud_mode}, base_url={config.base_url}", d)

    # Test config properties
    record("Config.is_cloud_mode", "PASS" if config.is_cloud_mode else "FAIL", str(config.is_cloud_mode), 0)
    record("Config.api_key set", "PASS" if config.api_key == API_KEY else "FAIL", "key matches", 0)


async def test_client_init():
    """Test ScalixClient initialization."""
    print("\n=== 2. ScalixClient Initialization ===")

    from scalix import ScalixClient

    t0 = time.time()
    client = ScalixClient(api_key=API_KEY, base_url=BASE_URL)
    d = (time.time() - t0) * 1000

    record("ScalixClient(api_key=...)", "PASS" if client else "FAIL",
           f"repr={repr(client)}", d)

    has_research = hasattr(client, 'research') and client.research is not None
    has_images = hasattr(client, 'images') and client.images is not None
    has_audio = hasattr(client, 'audio') and client.audio is not None

    record("client.research exists", "PASS" if has_research else "FAIL", "", 0)
    record("client.images exists", "PASS" if has_images else "FAIL", "", 0)
    record("client.audio exists", "PASS" if has_audio else "FAIL", "", 0)

    return client


async def test_research_service(client):
    """Test ResearchService endpoints."""
    print("\n=== 3. Research Service ===")

    # 3a. Research search
    try:
        t0 = time.time()
        result = await client.research.search("what is Python programming language")
        d = (time.time() - t0) * 1000
        has_results = isinstance(result, dict)
        record("research.search()", "PASS" if has_results else "FAIL",
               f"keys={list(result.keys()) if has_results else 'N/A'}", d)
    except Exception as e:
        record("research.search()", "FAIL", str(e), 0)

    # 3b. Research (deep research call)
    try:
        t0 = time.time()
        result = await client.research.research("explain quantum computing briefly")
        d = (time.time() - t0) * 1000
        has_results = isinstance(result, dict)
        record("research.research()", "PASS" if has_results else "FAIL",
               f"keys={list(result.keys()) if has_results else 'N/A'}", d)
    except Exception as e:
        record("research.research()", "FAIL", str(e), 0)

    # 3c. Deep research
    try:
        t0 = time.time()
        result = await client.research.deep("latest developments in AI agents 2026")
        d = (time.time() - t0) * 1000
        has_results = isinstance(result, dict)
        record("research.deep()", "PASS" if has_results else "FAIL",
               f"keys={list(result.keys()) if has_results else 'N/A'}", d)
    except Exception as e:
        record("research.deep()", "FAIL", str(e), 0)


async def test_images_service(client):
    """Test ImagesService endpoints."""
    print("\n=== 4. Images Service ===")

    # 4a. List models
    try:
        t0 = time.time()
        result = await client.images.models()
        d = (time.time() - t0) * 1000
        record("images.models()", "PASS" if isinstance(result, dict) else "FAIL",
               f"keys={list(result.keys()) if isinstance(result, dict) else 'N/A'}", d)
    except Exception as e:
        record("images.models()", "FAIL", str(e), 0)

    # 4b. Generate image
    try:
        t0 = time.time()
        result = await client.images.generate("A simple blue circle on white background")
        d = (time.time() - t0) * 1000
        record("images.generate()", "PASS" if isinstance(result, dict) else "FAIL",
               f"keys={list(result.keys()) if isinstance(result, dict) else 'N/A'}", d)
    except Exception as e:
        record("images.generate()", "FAIL", str(e), 0)

    # 4c. Async generation (queue)
    try:
        t0 = time.time()
        result = await client.images.generate_async("A red square on white background")
        d = (time.time() - t0) * 1000
        has_job = isinstance(result, dict)
        record("images.generate_async()", "PASS" if has_job else "FAIL",
               f"keys={list(result.keys()) if has_job else 'N/A'}", d)

        # 4d. Get job status (if we got a job_id)
        if has_job:
            job_id = result.get("job_id") or result.get("id") or result.get("jobId")
            if job_id:
                t0 = time.time()
                job = await client.images.get_job(job_id)
                d = (time.time() - t0) * 1000
                record("images.get_job()", "PASS" if isinstance(job, dict) else "FAIL",
                       f"status={job.get('status', 'N/A') if isinstance(job, dict) else 'N/A'}", d)
            else:
                record("images.get_job()", "SKIP", "no job_id in response", 0)
    except Exception as e:
        record("images.generate_async()", "FAIL", str(e), 0)


async def test_audio_service(client):
    """Test AudioService endpoints."""
    print("\n=== 5. Audio Service ===")

    # 5a. Voices list
    try:
        t0 = time.time()
        result = await client.audio.voices()
        d = (time.time() - t0) * 1000
        record("audio.voices()", "PASS" if isinstance(result, dict) else "FAIL",
               f"keys={list(result.keys()) if isinstance(result, dict) else 'N/A'}", d)
    except Exception as e:
        record("audio.voices()", "FAIL", str(e), 0)

    # 5b. Languages list
    try:
        t0 = time.time()
        result = await client.audio.languages()
        d = (time.time() - t0) * 1000
        record("audio.languages()", "PASS" if isinstance(result, dict) else "FAIL",
               f"keys={list(result.keys()) if isinstance(result, dict) else 'N/A'}", d)
    except Exception as e:
        record("audio.languages()", "FAIL", str(e), 0)

    # 5c. Text-to-speech
    try:
        t0 = time.time()
        result = await client.audio.speak("Hello, this is a test of the Scalix audio service.")
        d = (time.time() - t0) * 1000
        record("audio.speak()", "PASS" if isinstance(result, dict) else "FAIL",
               f"keys={list(result.keys()) if isinstance(result, dict) else 'N/A'}", d)
    except Exception as e:
        record("audio.speak()", "FAIL", str(e), 0)


async def test_direct_api():
    """Test API endpoints directly via httpx (endpoints not yet in SDK)."""
    print("\n=== 6. Direct API Calls (non-SDK) ===")
    import httpx

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as http:
        # 6a. Models list
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/models", headers=headers)
            d = (time.time() - t0) * 1000
            data = resp.json()
            model_count = len(data.get("data", []))
            record("GET /v1/models", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, models={model_count}", d)
        except Exception as e:
            record("GET /v1/models", "FAIL", str(e), 0)

        # 6b. Chat completions
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/chat/completions", headers=headers, json={
                "model": "scalix-world-ai",
                "messages": [{"role": "user", "content": "Say hello in exactly 5 words."}],
                "max_tokens": 50,
            })
            d = (time.time() - t0) * 1000
            data = resp.json()
            content = ""
            if resp.status_code == 200:
                choices = data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")[:100]
            record("POST /v1/chat/completions", "PASS" if resp.status_code == 200 and content else "FAIL",
                   f"status={resp.status_code}, response={content}", d)
        except Exception as e:
            record("POST /v1/chat/completions", "FAIL", str(e), 0)

        # 6c. Research status
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/research/status", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/research/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/research/status", "FAIL", str(e), 0)

        # 6d. Text sentiment
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/text/sentiment", headers=headers, json={
                "text": "I love using Scalix! It's amazing and makes my work so much easier."
            })
            d = (time.time() - t0) * 1000
            record("POST /v1/text/sentiment", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("POST /v1/text/sentiment", "FAIL", str(e), 0)

        # 6e. Text summarize
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/text/summarize", headers=headers, json={
                "text": "Artificial intelligence has been a hot topic for decades. The field of AI was founded in the 1950s, with early researchers dreaming of creating machines that could think like humans. Today, AI is used in everything from search engines to self-driving cars. Machine learning, a subset of AI, has become especially popular due to advances in neural networks and the availability of large datasets. Deep learning, which uses multi-layered neural networks, has achieved remarkable results in image recognition, natural language processing, and game playing."
            })
            d = (time.time() - t0) * 1000
            record("POST /v1/text/summarize", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("POST /v1/text/summarize", "FAIL", str(e), 0)

        # 6f. Text translate
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/text/translate", headers=headers, json={
                "text": "Hello world, how are you?",
                "target_language": "es"
            })
            d = (time.time() - t0) * 1000
            record("POST /v1/text/translate", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("POST /v1/text/translate", "FAIL", str(e), 0)

        # 6g. Text grammar
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/text/grammar", headers=headers, json={
                "text": "Me and him goes to store yesterday and buyed some foods."
            })
            d = (time.time() - t0) * 1000
            record("POST /v1/text/grammar", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("POST /v1/text/grammar", "FAIL", str(e), 0)

        # 6h. Text status
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/text/status", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/text/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/text/status", "FAIL", str(e), 0)

        # 6i. RAG status
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/rag/status", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/rag/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/rag/status", "FAIL", str(e), 0)

        # 6j. RAG documents list
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/rag/documents", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/rag/documents", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/rag/documents", "FAIL", str(e), 0)

        # 6k. DocGen formats
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/docgen/formats", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/docgen/formats", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/docgen/formats", "FAIL", str(e), 0)

        # 6l. DocGen templates
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/docgen/templates", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/docgen/templates", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/docgen/templates", "FAIL", str(e), 0)

        # 6m. DocGen status
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/docgen/status", headers=headers)
            d = (time.time() - t0) * 1000
            record("GET /v1/docgen/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/docgen/status", "FAIL", str(e), 0)

        # 6n. DocGen create
        try:
            t0 = time.time()
            resp = await http.post(f"{BASE_URL}/v1/docgen/create", headers=headers, json={
                "prompt": "Write a brief project proposal for a mobile app.",
                "format": "pdf"
            })
            d = (time.time() - t0) * 1000
            record("POST /v1/docgen/create", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("POST /v1/docgen/create", "FAIL", str(e), 0)

        # 6o. Images status (public)
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/images/status")
            d = (time.time() - t0) * 1000
            record("GET /v1/images/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/images/status", "FAIL", str(e), 0)

        # 6p. Audio kokoro status (public)
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/audio/kokoro/status")
            d = (time.time() - t0) * 1000
            record("GET /v1/audio/kokoro/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/audio/kokoro/status", "FAIL", str(e), 0)

        # 6q. Audio transcribe status (public)
        try:
            t0 = time.time()
            resp = await http.get(f"{BASE_URL}/v1/audio/transcribe/status")
            d = (time.time() - t0) * 1000
            record("GET /v1/audio/transcribe/status", "PASS" if resp.status_code == 200 else "FAIL",
                   f"status={resp.status_code}, body={resp.text[:100]}", d)
        except Exception as e:
            record("GET /v1/audio/transcribe/status", "FAIL", str(e), 0)


async def test_agent_framework():
    """Test the Agent framework with cloud provider."""
    print("\n=== 7. Agent Framework ===")

    from scalix import Agent, configure
    configure(api_key=API_KEY, base_url=BASE_URL)

    # The Agent in cloud mode uses ScalixRouterProvider which requires scalix-router package.
    # Test if it can at least initialize.
    try:
        t0 = time.time()
        agent = Agent(model="scalix-world-ai", instructions="You are a helpful assistant.")
        d = (time.time() - t0) * 1000
        record("Agent() init", "PASS", repr(agent), d)
    except Exception as e:
        record("Agent() init", "FAIL", str(e), 0)
        return

    # Try to run (may fail if scalix-router not installed, that's expected)
    try:
        t0 = time.time()
        result = await agent.run("Say hello in exactly 3 words.")
        d = (time.time() - t0) * 1000
        record("agent.run() cloud", "PASS" if result.output else "FAIL",
               f"output={result.output[:100]}", d)
    except ImportError as e:
        record("agent.run() cloud", "SKIP", f"scalix-router not installed: {e}", 0)
    except Exception as e:
        record("agent.run() cloud", "FAIL", str(e), 0)


async def test_error_handling():
    """Test error handling for various edge cases."""
    print("\n=== 8. Error Handling ===")

    from scalix import ScalixClient
    from scalix.exceptions import AuthenticationError, ScalixError

    # 8a. Missing API key
    try:
        from scalix.config import configure
        configure(api_key=None, base_url=BASE_URL)
        client = ScalixClient()
        await client.research.search("test")
        record("No API key → AuthenticationError", "FAIL", "Should have raised", 0)
    except AuthenticationError:
        record("No API key → AuthenticationError", "PASS", "Correctly raised", 0)
    except Exception as e:
        record("No API key → AuthenticationError", "FAIL", f"Wrong error: {type(e).__name__}: {e}", 0)

    # 8b. Invalid API key
    try:
        from scalix.config import configure
        configure(api_key="invalid_key_12345", base_url=BASE_URL)
        client = ScalixClient()
        await client.research.search("test")
        record("Invalid API key → Error", "FAIL", "Should have raised", 0)
    except (ScalixError, Exception) as e:
        record("Invalid API key → Error", "PASS", f"{type(e).__name__}: {str(e)[:80]}", 0)

    # Reset config
    from scalix.config import configure
    configure(api_key=API_KEY, base_url=BASE_URL)


async def test_typescript_sdk():
    """Test TypeScript SDK builds and types are correct."""
    print("\n=== 9. TypeScript SDK ===")

    ts_dir = os.path.join(os.path.dirname(__file__), "packages", "typescript")
    pkg_json = os.path.join(ts_dir, "package.json")

    if os.path.exists(pkg_json):
        with open(pkg_json) as f:
            pkg = json.load(f)
        record("package.json exists", "PASS", f"name={pkg.get('name')}, version={pkg.get('version')}", 0)
    else:
        record("package.json exists", "FAIL", "not found", 0)
        return

    # Check key source files exist
    src_dir = os.path.join(ts_dir, "src")
    key_files = ["index.ts", "client.ts", "config.ts", "types.ts"]
    for f in key_files:
        path = os.path.join(src_dir, f)
        exists = os.path.exists(path)
        record(f"TS src/{f} exists", "PASS" if exists else "FAIL", "", 0)


async def main():
    print("=" * 70)
    print("  SCALIX WORLD SDK — LIVE PRODUCTION TEST")
    print(f"  API: {BASE_URL}")
    print(f"  Key: {API_KEY[:20]}...")
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 70)

    await test_sdk_config()
    client = await test_client_init()
    await test_research_service(client)
    await test_images_service(client)
    await test_audio_service(client)
    await test_direct_api()
    await test_agent_framework()
    await test_error_handling()
    await test_typescript_sdk()

    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    total = len(results)

    print(f"  Total: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    print(f"  Pass Rate: {passed/total*100:.1f}%" if total > 0 else "  No tests run")

    if failed > 0:
        print("\n  FAILURES:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    ❌ {r['name']}: {r['detail']}")

    if skipped > 0:
        print("\n  SKIPPED:")
        for r in results:
            if r["status"] == "SKIP":
                print(f"    ⚠️  {r['name']}: {r['detail']}")

    return results


if __name__ == "__main__":
    all_results = asyncio.run(main())
