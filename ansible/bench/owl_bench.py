#!/usr/bin/env python3
# Owl's shared bench: the same requests to any engine's OpenAI-compatible API, so the engines compare.
# Decode: 3 fixed questions, greedy, thinking off, 256 tokens, after one warm-up answer.
# Prompt: the same text of about 2K, 8K and 16K tokens, twice each, with a new first line each time so that no
# prompt cache can answer it. Prompt speed is the prompt's tokens over the time to the first token.
# Standard library only: it runs with the machine's own python3.
import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
import uuid
from datetime import UTC, datetime

QUESTIONS = [
    "Write a Python function that parses a CSV file into a list of dictionaries, with type hints and a docstring.",
    "Explain how photosynthesis works, step by step, for a high-school student.",
    "Write a complete HTML page with a canvas that draws a bouncing ball animation in JavaScript.",
]
PROMPT_TOKENS = [2048, 8192, 16384]  # targets; each engine's tokenizer gives its own count, which the result records
WORDS = (
    "the model reads each token of the prompt before it writes an answer and the time it takes grows with the "
    "length of the text so a long document a log file or a code base costs more than a short question memory "
    "bandwidth sets the speed of each new token while compute sets the speed of reading the prompt"
).split()

ap = argparse.ArgumentParser()
ap.add_argument("--url", default="http://127.0.0.1:8731")
ap.add_argument("--key-file", help="a JSON file with an api_key field (Strata's saved preset)")
ap.add_argument("--out")
ap.add_argument("--set-context", nargs=3, metavar=("IN", "OUT", "TOKENS"),
                help="copy an engine's JSON config with each --max-context set to TOKENS, then exit")
ap.add_argument("--meta", default="{}", help="a JSON object to keep in the result (engine, version, model files)")
args = ap.parse_args()
if args.set_context:
    src, dst, tokens = args.set_context
    with open(src) as f:
        cfg = json.load(f)
    found = 0
    for v in cfg.values():  # Maya's "args"; Strata's "args", "args_written" and "args_derived"
        if isinstance(v, list) and "--max-context" in v[:-1]:
            v[v.index("--max-context") + 1] = tokens if isinstance(v[v.index("--max-context") + 1], str) else int(tokens)
            found += 1
    if not found:
        raise SystemExit(f"{src}: no --max-context to set")
    with open(dst, "w", opener=lambda p, fl: __import__("os").open(p, fl, 0o600)) as f:  # Strata's holds its key
        json.dump(cfg, f, indent=1)
    raise SystemExit(0)
if not args.out:
    ap.error("--out is required")
headers = {"Content-Type": "application/json"}
if args.key_file:
    with open(args.key_file) as f:
        headers["Authorization"] = "Bearer " + json.load(f)["api_key"]


def text(tokens):
    """The same words for every engine: a fixed sequence, about 5 characters a token."""
    out, i, n = [], 0, 0
    while n < tokens * 5:
        w = WORDS[(i * 7 + i // len(WORDS)) % len(WORDS)]
        out.append(w)
        n += len(w) + 1
        i += 1
    return " ".join(out)


def ready(timeout=1800):
    end = time.time() + timeout
    while time.time() < end:
        try:
            r = urllib.request.urlopen(urllib.request.Request(args.url + "/v1/models", headers=headers), timeout=10)
            return json.load(r)["data"][0]["id"]
        except (urllib.error.URLError, OSError, KeyError, IndexError, ValueError):
            time.sleep(5)
    raise SystemExit(f"no model at {args.url} after {timeout} s")


def chat(model, content, max_tokens):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": True,
        "stream_options": {"include_usage": True},
        "reasoning_effort": "none",
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(args.url + "/v1/chat/completions", json.dumps(body).encode(), headers)
    t0 = time.time()
    first = last = None
    pieces = reasoning = 0
    usage = {}
    with urllib.request.urlopen(req, timeout=1800) as r:
        for line in r:
            line = line.strip()
            if not line.startswith(b"data:") or line.endswith(b"[DONE]"):
                continue
            d = json.loads(line[5:])
            usage = d.get("usage") or usage
            for c in d.get("choices") or []:
                delta = c.get("delta") or {}
                r_text = delta.get("reasoning_content") or delta.get("reasoning") or ""
                if delta.get("content") or r_text:
                    first = first or time.time()
                    last = time.time()
                    pieces += 1
                    reasoning += len(r_text)
    out = usage.get("completion_tokens") or pieces
    return {
        "ttft_s": round(first - t0, 3) if first else None,
        "completion_tokens": out,
        "prompt_tokens": usage.get("prompt_tokens"),
        "decode_tok_s": round((out - 1) / (last - first), 1) if out > 1 and last > first else None,
        "reasoning_chars": reasoning,
    }


model = ready()
chat(model, "Say hello in one short sentence.", 32)  # warm-up
decode = [chat(model, q, 256) | {"question": q} for q in QUESTIONS]
prompts = []
for n in PROMPT_TOKENS:
    for _ in range(2):
        r = chat(model, f"Request {uuid.uuid4()}.\n{text(n)}\nSay OK.", 1)
        r["target_tokens"] = n
        if r["prompt_tokens"] and r["ttft_s"]:
            r["prompt_tok_s"] = round(r["prompt_tokens"] / r["ttft_s"])
        prompts.append(r)
rates = [d["decode_tok_s"] for d in decode if d["decode_tok_s"]]
result = json.loads(args.meta) | {
    "served_model": model,
    "date": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "settings": {"temperature": 0, "thinking": "off", "max_tokens": 256, "questions": QUESTIONS},
    "decode_tok_s_median": statistics.median(rates) if rates else None,
    "prompt_tok_s": {
        n: statistics.median([p["prompt_tok_s"] for p in prompts if p["target_tokens"] == n and "prompt_tok_s" in p])
        for n in PROMPT_TOKENS
        if any("prompt_tok_s" in p for p in prompts if p["target_tokens"] == n)
    },
    "thinking_seen": any(d["reasoning_chars"] for d in decode),
    "decode": decode,
    "prompts": prompts,
}
with open(args.out, "w") as f:
    json.dump(result, f, indent=1)
print(json.dumps({k: result[k] for k in ("served_model", "decode_tok_s_median", "prompt_tok_s", "thinking_seen")}))
