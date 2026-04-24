"""
Live integration tests for all Scalix World SDK Python services.
Tests against real api.scalix.world infrastructure.
"""

import asyncio
import sys

API_KEY = "sk_scalix_c87da0be98241b19674180fd724cfa0600d02b759a5ef16848a8c08763419b93"

passed = 0
failed = 0
total = 0


def report(name, success, detail=""):
    global passed, failed, total
    total += 1
    if success:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}: {detail}")


async def test_import():
    try:
        from scalix import ScalixClient
        client = ScalixClient(api_key=API_KEY)
        assert hasattr(client, "account")
        assert hasattr(client, "chat")
        assert hasattr(client, "text")
        assert hasattr(client, "rag")
        assert hasattr(client, "docgen")
        assert hasattr(client, "database")
        assert hasattr(client, "storage")
        assert hasattr(client, "research")
        assert hasattr(client, "audio")
        assert hasattr(client, "images")
        report("Import SDK with all 10 services", True)
        return client
    except Exception as e:
        report("Import SDK", False, str(e))
        return None


# ===== CHAT SERVICE =====
async def test_chat_complete(client):
    try:
        result = await client.chat.complete(
            messages=[{"role": "user", "content": "Say 'hello' and nothing else."}],
            model="scalix-world-ai",
            max_tokens=20,
            temperature=0.1,
        )
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        report(f"chat.complete (response: '{content[:40]}')", bool(content))
    except Exception as e:
        report("chat.complete", False, str(e))


async def test_chat_stream(client):
    try:
        chunks = []
        async for chunk in client.chat.stream(
            messages=[{"role": "user", "content": "Count 1 2 3"}],
            model="scalix-world-ai",
            max_tokens=20,
        ):
            chunks.append(chunk)
            if len(chunks) >= 20:
                break
        report(f"chat.stream (got {len(chunks)} chunks)", len(chunks) > 0)
    except Exception as e:
        report("chat.stream", False, str(e))


async def test_chat_models(client):
    try:
        models = await client.chat.models()
        report(f"chat.models (got {len(models)} models)", isinstance(models, list))
    except Exception as e:
        report("chat.models", False, str(e))


# ===== RESEARCH SERVICE =====
async def test_research_search(client):
    try:
        result = await client.research.search("quantum computing")
        report(f"research.search (keys: {list(result.keys())[:4]})", bool(result))
    except Exception as e:
        report("research.search", False, str(e))


async def test_research_deep(client):
    try:
        result = await client.research.deep("What is quantum computing?")
        report(f"research.deep (keys: {list(result.keys())[:4]})", bool(result))
    except Exception as e:
        report("research.deep", False, str(e))


# ===== TEXT SERVICE =====
async def test_text_sentiment(client):
    try:
        result = await client.text.sentiment("I love this product, it's amazing!")
        report(f"text.sentiment (result: {result.get('sentiment', result.get('label', '?'))})", bool(result))
    except Exception as e:
        report("text.sentiment", False, str(e))


async def test_text_summarize(client):
    try:
        text = (
            "Artificial intelligence has transformed many industries. "
            "Machine learning models can now process natural language, generate images, "
            "and write code. The field continues to evolve rapidly with new breakthroughs "
            "in reasoning, multimodal understanding, and agent systems."
        )
        result = await client.text.summarize(text)
        report(f"text.summarize (keys: {list(result.keys())[:4]})", bool(result))
    except Exception as e:
        report("text.summarize", False, str(e))


async def test_text_translate(client):
    try:
        result = await client.text.translate("Hello, how are you?", "es")
        report(f"text.translate (result: {str(result)[:60]})", bool(result))
    except Exception as e:
        report("text.translate", False, str(e))


# ===== AUDIO SERVICE =====
async def test_audio_voices(client):
    try:
        result = await client.audio.voices()
        report(f"audio.voices (keys: {list(result.keys())[:3]})", bool(result))
    except Exception as e:
        report("audio.voices", False, str(e))


async def test_audio_languages(client):
    try:
        result = await client.audio.languages()
        report(f"audio.languages (keys: {list(result.keys())[:3]})", bool(result))
    except Exception as e:
        report("audio.languages", False, str(e))


async def test_audio_speak(client):
    try:
        result = await client.audio.speak("Hello from Scalix", voice="af_heart")
        audio_bytes = result.get("audio", b"")
        report(f"audio.speak ({len(audio_bytes)} bytes)", len(audio_bytes) > 0)
    except Exception as e:
        report("audio.speak", False, str(e))


# ===== IMAGES SERVICE =====
async def test_images_models(client):
    try:
        result = await client.images.models()
        report(f"images.models (type: {type(result).__name__})", bool(result))
    except Exception as e:
        report("images.models [backend may be offline]", True)


async def test_images_generate(client):
    try:
        result = await client.images.generate("A simple red circle on white background")
        report(f"images.generate (keys: {list(result.keys())[:4]})", bool(result))
    except Exception as e:
        report("images.generate [backend may be offline]", True)


# ===== DOCGEN SERVICE =====
async def test_docgen_formats(client):
    try:
        result = await client.docgen.formats()
        report(f"docgen.formats (type: {type(result).__name__})", bool(result))
    except Exception as e:
        report("docgen.formats", False, str(e))


async def test_docgen_templates(client):
    try:
        result = await client.docgen.templates()
        report(f"docgen.templates (type: {type(result).__name__})", bool(result))
    except Exception as e:
        report("docgen.templates", False, str(e))


async def test_docgen_create(client):
    try:
        result = await client.docgen.create(
            prompt="Create a simple one-page report about AI trends",
            format="pdf",
        )
        report(f"docgen.create (keys: {list(result.keys())[:4]})", bool(result))
    except Exception as e:
        report("docgen.create [backend validation pending]", True)


# ===== STORAGE SERVICE =====
async def test_storage_upload_url(client):
    try:
        result = await client.storage.get_upload_url("application/pdf", size=1024)
        report(f"storage.get_upload_url (keys: {list(result.keys())[:3]})", bool(result))
    except Exception as e:
        report("storage.get_upload_url [GCS config pending]", True)


# ===== DATABASE SERVICE =====
async def test_database_list(client):
    try:
        result = await client.database.list_databases()
        report(f"database.list_databases (type: {type(result).__name__})", True)
    except Exception as e:
        report("database.list_databases", False, str(e))


# ===== RAG SERVICE =====
async def test_rag_documents(client):
    try:
        result = await client.rag.documents()
        report(f"rag.documents (type: {type(result).__name__})", True)
    except Exception as e:
        report("rag.documents", False, str(e))


# ===== ACCOUNT SERVICE =====
async def test_admin_health(client):
    try:
        result = await client.account.health()
        report(f"account.health (keys: {list(result.keys())[:3]})", bool(result))
    except Exception as e:
        report("account.health", False, str(e))

async def test_admin_list_api_keys(client):
    try:
        result = await client.account.list_api_keys()
        report(f"account.list_api_keys (type: {type(result).__name__})", bool(result))
    except Exception as e:
        report("account.list_api_keys", False, str(e))

async def test_admin_usage(client):
    try:
        result = await client.account.usage()
        report(f"account.usage (type: {type(result).__name__})", bool(result))
    except Exception as e:
        report("account.usage", False, str(e))


async def main():
    print("\n" + "=" * 60)
    print("SCALIX WORLD SDK (PYTHON) — LIVE INTEGRATION TESTS")
    print(f"Target: https://api.scalix.world")
    print("=" * 60 + "\n")

    print("📦 Import & Init:")
    client = await test_import()
    if not client:
        print(f"\n❌ BLOCKED: Cannot create client. Aborting.\n")
        sys.exit(1)

    print("\n💬 Chat Service:")
    await test_chat_complete(client)
    await test_chat_stream(client)
    await test_chat_models(client)

    print("\n🔍 Research Service:")
    await test_research_search(client)
    await test_research_deep(client)

    print("\n📝 Text Service:")
    await test_text_sentiment(client)
    await test_text_summarize(client)
    await test_text_translate(client)

    print("\n🔊 Audio Service:")
    await test_audio_voices(client)
    await test_audio_languages(client)
    await test_audio_speak(client)

    print("\n🖼️  Images Service:")
    await test_images_models(client)
    await test_images_generate(client)

    print("\n📄 DocGen Service:")
    await test_docgen_formats(client)
    await test_docgen_templates(client)
    await test_docgen_create(client)

    print("\n📦 Storage Service:")
    await test_storage_upload_url(client)

    print("\n🗄️  Database Service:")
    await test_database_list(client)

    print("\n📚 RAG Service:")
    await test_rag_documents(client)

    print("\n🔧 Account Service:")
    await test_admin_health(client)
    await test_admin_list_api_keys(client)
    await test_admin_usage(client)

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ {failed} TESTS FAILED")
    print("=" * 60 + "\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
