#!/usr/bin/env bash
# Regenerate the Python client FROM the committed spec at ../openapi.json.
#
# Output lands in scalix_sdk/generated/ and IS the package's public API since the
# cutover: scalix_sdk/__init__.py is a thin re-export of the generated
# Client/AuthenticatedClient. Generator: openapi-python-client (run via uvx, no Java).
#
# Usage:  cd sdk/python && ./scripts/generate.sh
#
# Verify after generating:
#   python3 -c "import ast,glob; [ast.parse(open(f,encoding='utf-8').read()) for f in glob.glob('scalix_sdk/generated/**/*.py', recursive=True)]"
#   uv run --no-project --with attrs --with httpx --with openai --with pydantic --with websockets \
#       python3 -c "import sys; sys.path.insert(0,'.'); import scalix_sdk.generated; print('ok')"
#
# NOTE on spec normalization:
#   openapi-python-client 0.29.0 (latest) cannot parse the JSON-Schema-2020-12
#   boolean form `items: false` (used on two tuple fields in components.schemas.WafStats:
#   top_blocked_ips and top_rules, each a fixed `[string, integer]` pair expressed
#   via prefixItems + `items: false`). `items: false` is redundant there — prefixItems
#   already fixes the tuple shape — so we strip ONLY that redundant keyword into a
#   temp copy before generating. The committed ../openapi.json is never modified, and
#   no generated output is hand-edited. The pairs render as list[list[int | str]].
set -euo pipefail

cd "$(dirname "$0")/.."

# Stamp the package version from the repo-root VERSION file (single source of
# truth), so pyproject.toml + _version.py never drift from the spec + TS SDK.
python3 scripts/sync_version.py

SPEC="../openapi.json"
NORMALIZED="$(mktemp -t scalix-openapi-XXXXXX.json)"
trap 'rm -f "$NORMALIZED"' EXIT

python3 - "$SPEC" "$NORMALIZED" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
n = 0
def walk(node):
    global n
    if isinstance(node, dict):
        if node.get("items") is False and "prefixItems" in node:
            del node["items"]; n += 1
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)
walk(d)
json.dump(d, open(dst, "w", encoding="utf-8"))
print(f"normalized spec: stripped {n} redundant 'items: false' tuple keyword(s)")
PY

# Pin the generator version so regeneration is deterministic (the CI drift-guard
# regenerates + git-diffs this output; an unpinned `uvx` would pull a newer
# generator and produce spurious diffs). Bump deliberately + commit the result.
uvx openapi-python-client@0.29.0 generate \
    --path "$NORMALIZED" \
    --meta none \
    --output-path scalix_sdk/generated \
    --overwrite

python3 - <<'PY'
from pathlib import Path

path = Path("scalix_sdk/generated/api/storage/put_object.py")
source = path.read_text(encoding="utf-8")
old = '_kwargs["content"] = body.payload'
if source.count(old) != 1 or source.count("body: File,") != 5:
    raise SystemExit("Unexpected put_object generator output; review binary upload serialization")
path.write_text(source.replace(old, old + ".read()"), encoding="utf-8")
PY

echo "Generated -> scalix_sdk/generated/ (re-exported as the package public API)"
