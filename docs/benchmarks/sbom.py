# Writes a CycloneDX 1.6 SBOM for one benchmark run: the machine, the engines and every model file.
# Each file's SHA-256 (sha256sum on the machine) is matched to a Hugging Face LFS oid at a pinned commit.
# A file with no match was made on the machine (a tokenizer extract, a Maya pack): the SBOM says so.
# Usage: uv run --no-project python -I sbom.py <sha256sums.txt> <date>.cdx.json
import json
import os
import sys
import urllib.request
import uuid
from datetime import UTC, datetime
from pathlib import Path

SUMS, OUT = sys.argv[1], sys.argv[2]
MACHINE = {
    "vendor": "GMKtec",
    "name": "EVO-X2",
    "bios": "EVO-X2S 1.13 (2026-06-26)",
    "cpu": "AMD Ryzen AI Max+ 395 w/ Radeon 8060S (gfx1151)",
    "ram": "128 GB LPDDR5X",
    "os": "Ubuntu 26.04.1 LTS",
    "kernel": "7.0.0-43-generic",
    "rocm": "7.14.1",
    "linux-firmware": "20260319.git217ca6e4",
    "ttm.pages_limit": "29637703",
}
ENGINES = [
    {
        "name": "project-maya",
        "version": "1.1.81",
        "purl": "pkg:github/mw00/project-maya@4a0ce6e86e1896309b8114914ce178bc69492e84",
        "url": "https://github.com/mw00/project-maya/tree/4a0ce6e86e1896309b8114914ce178bc69492e84",
    },
    {
        "name": "strata",
        "version": "0.2.22",
        "purl": "pkg:github/Niko1221/Strata@v0.2.22",
        "url": "https://github.com/Niko1221/Strata/releases/tag/v0.2.22",
    },
    {
        "name": "halogen-flash-server",
        "version": "0.20.7",
        "type": "container",
        "purl": "pkg:oci/halogen-flash-server@sha256%3A773073448dc9ff4a8c6b6c278802e254fd5f1546764e27531aeb3b77cb13482e"
        "?repository_url=ghcr.io/peonist-ai/halogen-flash-server&tag=0.20.7",
        "url": "https://github.com/peonist-ai/halogen-flash-server",
    },
]
# The commits that Maya v1.1.81 pins (tools/*/download*.json, maya.py) and Owl pins; "main" is resolved at run time.
REPOS = [
    (
        "peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF",
        "c33d87b8c7a3b7d55e71324dc82395587a870b0b",
    ),
    (
        "orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF",
        "349470a09c1fca35862b0796e726b9fe00a947df",
    ),
    ("peasantsmith/GLM-5.3-Flash-Maya-GGUF", "main"),
    ("peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF", "main"),
    ("peasantsmith/Hy4-Flash-Maya-GGUF", "9d73294d20e1119d03d00ea81d1d352bfbe61ff4"),
    ("unsloth/Inkling-2-Mini-GGUF", "ae9327c5fbc7333116ba32eee78bb5d2bbefae4f"),
    (
        "peonist-ai/halogen-qwen3.8-flash-next",
        "fe3653f365c8f9d508712ffeded88ec93cf33852",
    ),
    (
        "Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated",
        "e7783c5822dfda2785a0f5b435abf54df89fe8ee",
    ),
    # Strata downloads from these without a pinned commit; "main" is the commit whose files match.
    ("ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF", "main"),
    ("unsloth/Qwen3.8-Flash-Next-GGUF", "main"),
    ("strata-engine/Hy4-Flash-Strata", "main"),
    ("strata-engine/Inkling-2-Mini-Strata", "main"),
]

# Files that an engine pins by SHA-256 in its own code, not by a Hugging Face file.
PINNED = {
    "4df2e5ab2b47c064afbe662e16e4f06569877125c2d0e2123a4ac755266c664c": "Strata 0.2.22's tuned DFlash2 pack (TUNED_SHA256),"
    " made from incoai/Qwen3.8-Flash-Next-DFlash2@a22a1744e85c17364dcc54a6a420af7135d4c7f6",
}

token_file = os.path.expanduser("~/.cache/huggingface/token")
token = (
    Path(token_file).read_text().strip() if os.path.exists(token_file) else None
)  # orcarouter's repo is gated


def get(url):
    headers = {"User-Agent": "owl-sbom"} | (
        {"Authorization": "Bearer " + token} if token else {}
    )
    return json.load(
        urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60)
    )


oids = {}
for repo, rev in REPOS:
    sha = get(f"https://huggingface.co/api/models/{repo}/revision/{rev}")["sha"]
    for f in get(f"https://huggingface.co/api/models/{repo}/tree/{sha}?recursive=true"):
        if (f.get("lfs") or {}).get("oid"):
            oids.setdefault(f["lfs"]["oid"], []).append((repo, sha, f["path"]))

components = [
    {
        "type": e.get("type", "application"),
        "name": e["name"],
        "version": e["version"],
        "purl": e["purl"],
        "externalReferences": [
            {"type": "vcs" if "github" in e["url"] else "website", "url": e["url"]}
        ],
    }
    for e in ENGINES
]
unmatched = 0
for line in Path(SUMS).read_text().splitlines():
    digest, path = line.split(None, 1)
    path = path.strip()
    c = {
        "type": "data",
        "name": path,
        "hashes": [{"alg": "SHA-256", "content": digest}],
    }
    if digest in oids:
        # Identical files can sit in several folders (a shared shard): take the one with the same name.
        same = [
            m
            for m in oids[digest]
            if m[2].rsplit("/", 1)[-1] == path.rsplit("/", 1)[-1]
        ]
        repo, sha, hf_path = (same or oids[digest])[0]
        c |= {
            "type": "machine-learning-model"
            if path.endswith((".gguf", ".hgn", ".dfly2", ".bin"))
            else "data",
            "purl": f"pkg:huggingface/{repo}@{sha}",
            "version": sha,
            "externalReferences": [
                {
                    "type": "distribution",
                    "url": f"https://huggingface.co/{repo}/blob/{sha}/{hf_path}",
                }
            ],
        }
    elif digest in PINNED:
        c["properties"] = [{"name": "owl:origin", "value": PINNED[digest]}]
    elif path.startswith("halogen/npu/"):
        c["properties"] = [
            {
                "name": "owl:origin",
                "value": "fetched by halogen 0.20.7 at start (HALOGEN_NPU_MODELS)",
            }
        ]
    else:
        unmatched += 1
        c["properties"] = [
            {
                "name": "owl:origin",
                "value": "made on the machine by the engine's setup (no upstream file)",
            }
        ]
    components.append(c)

sbom = {
    "$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json",
    "bomFormat": "CycloneDX",
    "specVersion": "1.6",
    "serialNumber": f"urn:uuid:{uuid.uuid4()}",
    "version": 1,
    "metadata": {
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "component": {
            "type": "device",
            "name": "owl",
            "manufacturer": {"name": MACHINE["vendor"]},
            "properties": [
                {"name": f"owl:{k}", "value": v} for k, v in MACHINE.items()
            ],
        },
    },
    "components": components,
}
Path(OUT).write_text(json.dumps(sbom, indent=1))
print(
    f"{len(components)} components, {sum('purl' in c and 'huggingface' in c['purl'] for c in components)} matched "
    f"to Hugging Face, {unmatched} made on the machine"
)
