# Benchmark run: 2026-11-26 on owl

One GMKtec EVO-X2 (Ryzen AI Max+ 395, Radeon 8060S, 128 GB). Every model ran alone on the machine, with no other engine.
Each engine used its own bench. The raw output of each bench is in this folder.

## Results

Decode is the median of three answers of 256 tokens, greedy, with thinking off. The range is in brackets.
Prompt is the speed to read a prompt of 2K and 8K tokens.

| Engine | Model | Context | Drafting (drafts accepted) | Decode tok/s | Prompt 2K / 8K tok/s | Load | Raw output |
|---|---|---|---|---|---|---|---|
| halogen 0.20.7 | Qwen3.8-Flash-Next v2, abliterated | 256K | MTP | **64.8** mean (52.9–80.6) | 1655 / 2347 ¹ | 258 s | [halogen.txt](halogen.txt), [halogen-prompt.txt](halogen-prompt.txt) |
| Maya v1.1.77 | Inkling 2 Mini UD-Q4_K_XL | 256K | DSpark drafter (63%) | **49.3** (41.4–63.8) | 1130 / 1049 | 16 s | [maya-inkling.txt](maya-inkling.txt) |
| Maya v1.1.77 | DeepSeek-V4.1-Flash-1017 Maya-XS | 256K | DSpark (84%) | **33.5** (24.8–38.6) | 282 / 439 | 49 s | [maya-deepseek.txt](maya-deepseek.txt) |
| Maya v1.1.77 | DeepSeek-V4.1-Flash-1017 abliterated Mix-128G | 256K | DSpark (82%) | **32.3** (23.6–37.8) | 284 / 428 | 43 s | [maya-deepseek-abl.txt](maya-deepseek-abl.txt) |
| Maya v1.1.77 | GLM-5.3-Flash Maya-S-v2 IQ2_XXS | 32K | MTP (84%) | **27.2** (25.6–30.4) | 264 / 270 | 40 s | [maya-glm.txt](maya-glm.txt) |
| Maya v1.1.77 | Hy4-Flash Maya-L | 32K | MTP (81%) | **22.4** (20.5–25.0) | 162 / 305 | 415 s | [maya-hy4.txt](maya-hy4.txt) |
| Maya v1.1.77 | GLM-5.3-Flash Maya-M-Derisked IQ2_S | 256K | MTP (83%) | **16.0** (13.3–16.8) | 202 / 266 | 38 s | [maya-glm-derisked-256k.txt](maya-glm-derisked-256k.txt) |
| Maya v1.1.77 | GLM-5.3-Flash Maya-M-Derisked IQ2_S | 512K | MTP (85%) | 13.1 (12.4–15.0) | 173 / 200 | 39 s | [maya-glm-derisked.txt](maya-glm-derisked.txt) |

¹ halogen's bench does not measure prompts. These numbers come from [halogen-prompt.py](../halogen-prompt.py), with
prompts of 2602 and 10938 tokens. The same script measured 72.9–96.6 tok/s decode on three short questions.

halogen's decode is the mean of its bench: 10 cases (code, proofs, procedures, chat, prose), 256 tokens each, effort
`low`. Without drafting it decodes 30.9–32.7 tok/s. Its bench checks that every drafted answer is byte-identical to the
answer without drafting: PASS.

### Notes

- The 192 GB Gorgon Halo results in Maya's README are faster, because that machine keeps all the experts in memory.
  On owl, DeepSeek Maya-XS keeps 13,054 of 15,744 experts on the GPU and reads 19 GB from the SSD.
- Maya-M-Derisked at 512K: 90.8% of experts are in VRAM, and each token reads about 14 experts from the SSD (48 ms of
  99 ms). At 256K the smaller KV cache leaves more memory for experts: decode +22%, 8K prompt +33%.
  Owl now serves it at 256K.
- Strata was not part of this run.

## Software

| Part | Version | Proof |
|---|---|---|
| Project Maya | v1.1.77 | commit [`cfc825fbc90b56fd7e2625ca026b9924c7211ebb`](https://github.com/mw00/project-maya/tree/cfc825fbc90b56fd7e2625ca026b9924c7211ebb) |
| halogen-flash-server | 0.20.7 | `ghcr.io/peonist-ai/halogen-flash-server@sha256:773073448dc9ff4a8c6b6c278802e254fd5f1546764e27531aeb3b77cb13482e` |
| ROCm | 7.14.1 | tarball SHA-256 `c40e8f2bd6630a7d11557c762b99c6fa8afb04c9bd0e51ed1675ee1ca24afb00` (Owl's pin) |
| Ubuntu | 26.04.1 LTS, kernel 7.0.0-43-generic | |
| linux-firmware | 20260319.git217ca6e4 | |
| BIOS | EVO-X2S 1.13 (2026-06-26) | |
| GPU memory limit | `ttm pages_limit=29637703` (113 GiB) | |

## Models

On the machine, `sha256sum` hashed every model file: [sha256sums.txt](sha256sums.txt). Each weight file matches the
Hugging Face LFS SHA-256 of that file at the commit below. [sbom.cdx.json](sbom.cdx.json) is the full list as a
CycloneDX 1.6 SBOM. It also lists the 20 files that the engines' setup made on the machine (tokenizer extracts,
Maya's `pack/dense.bin`, `tensors.txt`, `vision.bin`), which have no upstream copy.

| Model | Hugging Face repo | Commit | Weight files (SHA-256, first 16) |
|---|---|---|---|
| halogen Qwen3.8-Flash-Next | [peonist-ai/halogen-qwen3.8-flash-next](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next/tree/05ec74b75cd68c4d6486d15825f2fc73b2ffe304) | `05ec74b75cd68c4d6486d15825f2fc73b2ffe304` | drafter-r2-ht4 `f9aa330800cc921f`, mtp `0f50e9626df98168`, ngram `3450acada94e19aa`, vision `d62e0ae553fe88af` |
| halogen abliterated checkpoint | [Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated](https://huggingface.co/Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated/tree/e7783c5822dfda2785a0f5b435abf54df89fe8ee) | `e7783c5822dfda2785a0f5b435abf54df89fe8ee` | v2-abliterated `7bbac319851b5006` |
| Inkling 2 Mini | [unsloth/Inkling-2-Mini-GGUF](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF/tree/ae9327c5fbc7333116ba32eee78bb5d2bbefae4f) | `ae9327c5fbc7333116ba32eee78bb5d2bbefae4f` | UD-Q4_K_XL `e62d463c135ffe28`, dspark Q8_0 `2ec78510da837e8f`, mmproj `2c165c78790e78a3` |
| DeepSeek Maya-XS | [peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF](https://huggingface.co/peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF/tree/c33d87b8c7a3b7d55e71324dc82395587a870b0b) | `c33d87b8c7a3b7d55e71324dc82395587a870b0b` | shards `9d92dd13d4603dbf` `b7f26bae6d6fccfb` `62b9817256254312`, Engram `0d93315942c523d8` `39bbc8cde8b17604`, dspark-xs2 `8dfe21082a6cb320` |
| DeepSeek abliterated | [orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF](https://huggingface.co/orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF/tree/349470a09c1fca35862b0796e726b9fe00a947df) (gated) | `349470a09c1fca35862b0796e726b9fe00a947df` | Mix-128G shards 1, 3, 4, 5: `0d4eedd085f38e31` `3c86e27595d9e45a` `d7fab155dcebfea8` `ecbf6562afd1b055`; Engram and dspark from DeepSeek Maya-XS |
| GLM-5.3-Flash Maya-S-v2 | [peasantsmith/GLM-5.3-Flash-Maya-GGUF](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-GGUF/tree/6f6c6a8394c32f556c09bea0a06dce0b76a3dc37) | `6f6c6a8394c32f556c09bea0a06dce0b76a3dc37` ² | shards `e56ef50efd71d81d` `2d65d88a69f8dc12` `a6a981c4fee7a53d`, mmproj `3627575df16bd152`, vocab `8f53cb1bd2e631c1` |
| GLM-5.3-Flash Maya-M-Derisked | [peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF/tree/b0a5474568ab4322ba4b74be5f34308fb4592d57) | `b0a5474568ab4322ba4b74be5f34308fb4592d57` ² | shards `da6a9755946f85a6` `afc0705798bb2934` `e397c79669b84e8f`; vision files from Maya-S |
| Hy4-Flash Maya-L | [peasantsmith/Hy4-Flash-Maya-GGUF](https://huggingface.co/peasantsmith/Hy4-Flash-Maya-GGUF/tree/9d73294d20e1119d03d00ea81d1d352bfbe61ff4) | `9d73294d20e1119d03d00ea81d1d352bfbe61ff4` | Maya-L shards `5f47ce10c0cb6186` `5819578b52eb1cda` ³, mtp `a49e5ae439de9a51`, drafter `c856ae476a42ea69`, mmproj `6884c0317a4e3e78` |

² Maya v1.1.77 downloads the GLM models from `main`, with no pinned commit. The commit is the one whose files match.
³ On the machine, Maya-L's second shard has the name `Hy4-Flash-Maya-XS-IQ2_XXS-00002-of-00002.gguf`. Its hash is the
hash of `Maya-L/Hy4-Flash-Maya-L-IQ4_XS-00002-of-00002.gguf`.

## Run it again

On the machine, stop all engines first. Each bench needs all of the memory.

```sh
sudo systemctl stop halogen maya strata
cd ~/src/project-maya && ./maya.sh --bench --config .installed-<commit>-<hash>.json   # one model; writes maya-bench.txt
podman run --rm --device /dev/kfd --device /dev/dri --group-add keep-groups --ipc=host --ulimit memlock=-1:-1 \
  -e HALOGEN_CHECKPOINT=/models/qwen38-flash-next-v2-abliterated.hgn -e HALOGEN_WEIGHTS_LOCK=1 \
  -v ~/models/halogen:/models ghcr.io/peonist-ai/halogen-flash-server:0.20.7 bench
sudo systemctl start halogen && python3 halogen-prompt.py
cd ~/models && find maya halogen -type f -size +1M -not -path '*/.cache/*' -print0 | xargs -0 -P 8 -n 1 sha256sum > sha256sums.txt
```

Then make the SBOM on your computer: `uv run --no-project python -I docs/benchmarks/sbom.py docs/benchmarks/<date>`.
