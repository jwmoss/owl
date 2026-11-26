# The halogen numbers that halogen's own bench does not give: decode on three 256-token answers and prompt speed.
# Run it on the machine while halogen serves: python3 halogen-prompt.py
import json
import time
import urllib.request


def req(msgs, maxt):
    b = json.dumps(
        {
            "model": "halogen-qwen3.8-flash-next",
            "messages": msgs,
            "max_tokens": maxt,
            "temperature": 0,
            "reasoning_effort": "low",
            "stream": True,
            "stream_options": {"include_usage": True},
        }
    ).encode()
    r = urllib.request.urlopen(
        urllib.request.Request(
            "http://localhost:8731/v1/chat/completions",
            b,
            {"Content-Type": "application/json"},
        ),
        timeout=600,
    )
    t0 = time.time()
    first = None
    usage = None
    for line in r:
        line = line.strip()
        if not line.startswith(b"data:") or line.endswith(b"[DONE]"):
            continue
        d = json.loads(line[5:])
        if d.get("usage"):
            usage = d["usage"]
        if (
            first is None
            and d.get("choices")
            and (
                d["choices"][0]["delta"].get("content")
                or d["choices"][0]["delta"].get("reasoning_content")
            )
        ):
            first = time.time()
    return t0, first, time.time(), usage


for q in [
    "Write a Python function that parses an ISO 8601 date and explain it.",
    "Explain how TCP congestion control works.",
    "Write an HTML page with a CSS animated spinner.",
]:
    t0, f, t1, u = req([{"role": "user", "content": q}], 256)
    n = u["completion_tokens"]
    print(f"decode {n / (t1 - f):.1f} tok/s ({n} tokens), first token {f - t0:.2f} s")
for words in (1500, 6000):
    txt = " ".join(
        f"Line {i}: the quick brown fox number {i} jumps over lazy dog {i * 7 % 13}."
        for i in range(words // 12)
    )
    t0, f, t1, u = req([{"role": "user", "content": txt + "\nSay OK."}], 1)
    p = u["prompt_tokens"]
    print(f"prompt {p} tokens in {f - t0:.2f} s = {p / (f - t0):.0f} tok/s")
