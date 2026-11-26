# Benchmark run: 2026-11-26 on owl

> **Machine:** GMKtec EVO-X2 · AMD Ryzen AI Max+ 395 · Radeon 8060S (gfx1151) · 128 GB LPDDR5X · Ubuntu 26.04.1 · ROCm 7.14.1
>
> **Engines:** halogen 0.20.7 · Project Maya v1.1.81 · Strata 0.2.22. These are the versions that Owl's `main` pins.

Each model ran alone on the machine, with no other engine. Each engine used its own bench, and this folder holds
the raw output of each one. Every model file was hashed on the machine, and each weight file is byte-identical to the
Hugging Face file named in [Models](#models).

## Results

| Engine | Model | Quant | Context | Drafting | Decode tok/s | Prompt tok/s | Raw output |
|---|---|---|---:|---|---:|---:|---|
| halogen | [Qwen3.8-Flash-Next](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next) | v2 `.hgn` | 256K | MTP head r2-ht4 | **73.0** | 1646 / 2350 | [bench](halogen-v2.txt) · [prompt](halogen-prompt-v2.txt) |
| halogen | [Qwen3.8-Flash-Next abliterated](https://huggingface.co/Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated) ★ | v2 `.hgn` | 256K | MTP head r2-ht4 | **71.1** | 1651 / 2354 | [bench](halogen-v2-abliterated.txt) · [prompt](halogen-prompt-v2-abliterated.txt) |
| Strata | [Qwen3.8-Flash-Next GSQ-RCO](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) | IQ3_S | 128K | DFlash2 | **49.5** | 799 / 806 | [report](strata-qwen/README.md) |
| Maya | [Inkling 2 Mini](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | UD-Q4_K_XL | 256K | DSpark (72%) | **47.8** | 1078 / 1038 | [bench](maya-inkling.txt) |
| Maya | [DeepSeek-V4.1-Flash-1017](https://huggingface.co/peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF) | Maya-XS v2 | 256K | DSpark (85%) | **32.9** | 264 / 448 | [bench](maya-deepseek.txt) |
| Maya | [DeepSeek-V4.1-Flash-1017 abliterated](https://huggingface.co/orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF) | Mix-128G | 256K | DSpark (83%) | **29.5** | 262 / 452 | [bench](maya-deepseek-abl.txt) |
| Strata | [Inkling 2 Mini](https://huggingface.co/strata-engine/Inkling-2-Mini-Strata) | SQ-20 | 128K | — | **28.0** | 780 / 758 ¹ | [report](strata-inkling/README.md) |
| Maya | [GLM-5.3-Flash](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-GGUF) | Maya-S v2 IQ2_XXS | 32K | MTP (83%) | **27.1** | 266 / 270 | [bench](maya-glm.txt) |
| Strata | [Hy4-Flash](https://huggingface.co/strata-engine/Hy4-Flash-Strata) | SQ-96 | 128K | — | **25.8** | 589 / 600 ¹ | [report](strata-hy4/README.md) |
| Maya | [Hy4-Flash](https://huggingface.co/peasantsmith/Hy4-Flash-Maya-GGUF) | Maya-L IQ4_XS | 32K | MTP (80%) | **22.4** | 164 / 205 | [bench](maya-hy4.txt) |
| Maya | [GLM-5.3-Flash Maya-M-Derisked](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF) ★ | IQ2_S | 256K | MTP (85%) | **16.9** | 195 / 250 | [bench](maya-glm-derisked.txt) |

★ The model that owl serves on that engine.

### How each engine measures

These benches are not the same test. Compare rows of one engine only.

| | halogen `bench` | Maya `--bench` | Strata `standard-v1` |
|---|---|---|---|
| Decode prompts | 10 fixed prompts in 5 shapes: code, proofs, procedures, chat, prose | 3 fixed questions: a Python CSV parser, photosynthesis, an HTML bouncing ball | 1 question: how a hash table finds a value |
| Sampling | greedy | greedy | temperature 1.0 |
| Thinking | effort `low` | off | on, effort `xhigh` |
| Answer | 256 tokens | 256 tokens | up to 512 tokens, thinking included |
| Long prompts | none (see [halogen-prompt.py](../halogen-prompt.py)) | 2K / 8K tokens cut from Maya's docs | 4K / 16K tokens of `recordNNNNNN: alpha beta …` |
| Context | the served one (256K) | the served one (32K or 256K) | the served one (128K) |


Decode is the mean of halogen's 10 cases, and the median of Maya's 3 answers and Strata's 3 short requests.

¹ Strata's suite makes its prompts with Qwen's tokenizer. With Hy4's and Inkling's own tokenizers they are shorter
(2.8K / 11.2K and 3.4K / 13.8K tokens), so Strata marks these two runs "nonconforming". All 21 requests finished,
and all 12 sanity checks passed (instruction, retrieval and tool calls) on all three Strata presets.

### Notes

- halogen checks that each drafted answer is byte-identical to the answer without drafting: PASS on both checkpoints.
  Without drafting it writes about 40 tok/s.
- The abliterated halogen checkpoint is about 3% slower than stock v2. With one run each, that is close to the noise.
- DeepSeek Maya-XS keeps 13,054 of 15,744 experts on the GPU and reads about 19 GB from the SSD, because 128 GB does
  not hold all of it. The 192 GB Gorgon Halo results in Maya's README keep every expert in memory.
- GLM Maya-M-Derisked reads some experts from the SSD at each token. At 512K context it wrote 13.1 tok/s
  (Maya v1.1.77), so owl now serves it at 256K.

## Models

The SHA-256 is the first 16 characters. The full sums are in [sha256sums.txt](sha256sums.txt), and the complete list,
with the 28 files that the engines' setup makes on the machine, is in two standard SBOMs:
[sbom.cdx.json](sbom.cdx.json) (CycloneDX 1.6) and [sbom.spdx.json](sbom.spdx.json) (SPDX 2.3). Both pass their
format's validator (`cyclonedx-python-lib` strict schema, `pyspdxtools`).

| Engine | Hugging Face repo | Commit | Weight files | SHA-256 |
|---|---|---|---|---|
| halogen | [`peonist-ai/halogen-qwen3.8-flash-next`](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next/tree/fe3653f365c8f9d508712ffeded88ec93cf33852) | `fe3653f` | `qwen38-flash-next-v2.hgn`<br>`qwen38-flash-next-ngram.hgn`<br>`qwen38-flash-next-drafter-r2-ht4.hgn`<br>`qwen38-flash-next-vision.hgn` | `71246c6ab3fc1de2`<br>`3450acada94e19aa`<br>`6feed319c3d8fa6c`<br>`d62e0ae553fe88af` |
| halogen | [`Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated`](https://huggingface.co/Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated/tree/e7783c5822dfda2785a0f5b435abf54df89fe8ee) | `e7783c5` | `qwen38-flash-next-v2-abliterated.hgn` | `7bbac319851b5006` |
| Strata | [`ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF`](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/tree/ed59f92082b1e93c0e96d60a8b11aab089b52f09) ² | `ed59f92` | `IQ3_S/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf`<br>`IQ3_S/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00002-of-00002.gguf`<br>`mmproj-Qwen3.8-Flash-Next-BF16.gguf` | `4c1eb2ceb4915e11`<br>`316b46f3a2dbd68c`<br>`b1a82259702816a5` |
| Strata | DFlash2 draft pack, from [`incoai/Qwen3.8-Flash-Next-DFlash2`](https://huggingface.co/incoai/Qwen3.8-Flash-Next-DFlash2/tree/a22a1744e85c17364dcc54a6a420af7135d4c7f6) | `a22a174` | `qwen3.8-flash-next-dflash2.strata1.q4_0-selq4.pack` (Strata pins this SHA-256) | `4df2e5ab2b47c064` |
| Strata | [`strata-engine/Hy4-Flash-Strata`](https://huggingface.co/strata-engine/Hy4-Flash-Strata/tree/995bac227ab7e0d221772be641e2b5954a9fac06) ² | `995bac2` | `Hy4-Flash-SQ-96.strata`<br>`Hy4-Flash-Engram-Q8.strata`<br>`Hy4-Flash-Vision.strata` | `3b1c5755a220c698`<br>`ab0cf9b3f9c64bd2`<br>`ef09bceff8f01b8d` |
| Strata | [`strata-engine/Inkling-2-Mini-Strata`](https://huggingface.co/strata-engine/Inkling-2-Mini-Strata/tree/04996a1e2c45009b6a04f2af126cb6bdb2ba3587) ² | `04996a1` | `Inkling-2-Mini-SQ-20.strata`<br>`Inkling-2-Mini-Vision.strata` | `0bbfd52344f0dd47`<br>`6589eff47f9c20bc` |
| Maya | [`unsloth/Inkling-2-Mini-GGUF`](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF/tree/ae9327c5fbc7333116ba32eee78bb5d2bbefae4f) | `ae9327c` | `Inkling-2-Mini-UD-Q4_K_XL.gguf`<br>`dspark-Inkling-2-Mini-Q8_0.gguf`<br>`mmproj-BF16.gguf` | `e62d463c135ffe28`<br>`2ec78510da837e8f`<br>`2c165c78790e78a3` |
| Maya | [`peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF`](https://huggingface.co/peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF/tree/c33d87b8c7a3b7d55e71324dc82395587a870b0b) | `c33d87b` | `Maya-XS/DeepSeek-V4.1-Flash-1017-Maya-XS-v2-IQ1_S-00001-of-00003.gguf`<br>`Maya-XS/…-Maya-XS-v2-IQ1_S-00002-of-00003.gguf`<br>`Maya-XS/…-Maya-XS-v2-IQ1_S-00003-of-00003.gguf`<br>`Maya-XS/…-Maya-XS-IQ1_S-00004-of-00005.gguf` (Engram)<br>`Maya-XS/…-Maya-XS-IQ1_S-00005-of-00005.gguf` (Engram)<br>`dspark/dspark-xs2.bin` | `9d92dd13d4603dbf`<br>`b7f26bae6d6fccfb`<br>`62b9817256254312`<br>`0d93315942c523d8`<br>`39bbc8cde8b17604`<br>`8dfe21082a6cb320` |
| Maya | [`orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF`](https://huggingface.co/orcarouter/DeepSeek-V4.1-Flash-1017-abliterated-GGUF/tree/349470a09c1fca35862b0796e726b9fe00a947df) (gated) | `349470a` | `Mix-128G/DeepSeek-V4.1-Flash-1017-abliterated-Mix-128G-00001-of-00005.gguf`<br>`Mix-128G/…-Mix-128G-00003-of-00005.gguf`<br>`Mix-128G/…-Mix-128G-00004-of-00005.gguf`<br>`Mix-128G/…-Mix-128G-00005-of-00005.gguf`<br>Engram from Maya-XS; `dspark/dspark.bin` from peasantsmith | `0d4eedd085f38e31`<br>`3c86e27595d9e45a`<br>`d7fab155dcebfea8`<br>`ecbf6562afd1b055`<br><br>`42df65159f980a91` |
| Maya | [`peasantsmith/GLM-5.3-Flash-Maya-GGUF`](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-GGUF/tree/6f6c6a8394c32f556c09bea0a06dce0b76a3dc37) ² | `6f6c6a8` | `Maya-S-v2-IQ2_XXS/GLM-5.3-Flash-Maya-S-v2-IQ2_XXS-00001-of-00003.gguf`<br>`Maya-S-v2-IQ2_XXS/…-00002-of-00003.gguf`<br>`Maya-S-v2-IQ2_XXS/…-00003-of-00003.gguf`<br>`vision/mmproj-GLM-5.3-Flash-F16.gguf` | `e56ef50efd71d81d`<br>`2d65d88a69f8dc12`<br>`a6a981c4fee7a53d`<br>`3627575df16bd152` |
| Maya | [`peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF`](https://huggingface.co/peasantsmith/GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-GGUF/tree/b0a5474568ab4322ba4b74be5f34308fb4592d57) ² | `b0a5474` | `GLM-5.3-Flash-Maya-M-Derisked-IQ2_S-00001-of-00003.gguf`<br>`…-00002-of-00003.gguf`<br>`…-00003-of-00003.gguf`<br>vision files from Maya-S | `da6a9755946f85a6`<br>`afc0705798bb2934`<br>`e397c79669b84e8f` |
| Maya | [`peasantsmith/Hy4-Flash-Maya-GGUF`](https://huggingface.co/peasantsmith/Hy4-Flash-Maya-GGUF/tree/9d73294d20e1119d03d00ea81d1d352bfbe61ff4) | `9d73294` | `Maya-L/Hy4-Flash-Maya-L-IQ4_XS-00001-of-00002.gguf`<br>`Maya-L/Hy4-Flash-Maya-L-IQ4_XS-00002-of-00002.gguf` ³<br>`mtp/Hy4-Flash-mtp-BF16.gguf_file`<br>`Maya-L/Hy4-Flash-Maya-L-drafter.dfly2`<br>`Maya-XS/mmproj-Hy4-Flash-Maya-XS.gguf` | `5f47ce10c0cb6186`<br>`5819578b52eb1cda`<br>`a49e5ae439de9a51`<br>`c856ae476a42ea69`<br>`6884c0317a4e3e78` |

² The engine downloads this repo from `main`, with no pinned commit. The commit shown is the one whose files match.
³ On the machine this file has the name `Hy4-Flash-Maya-XS-IQ2_XXS-00002-of-00002.gguf`. Its SHA-256 is the SHA-256 of
the Maya-L shard.

## Software

| Part | Version | Proof |
|---|---|---|
| halogen-flash-server | 0.20.7 | `ghcr.io/peonist-ai/halogen-flash-server@sha256:773073448dc9ff4a8c6b6c278802e254fd5f1546764e27531aeb3b77cb13482e` |
| Project Maya | v1.1.81 | [`4a0ce6e86e1896309b8114914ce178bc69492e84`](https://github.com/mw00/project-maya/tree/4a0ce6e86e1896309b8114914ce178bc69492e84) |
| Strata | 0.2.22 (control 0.1.69) | [release v0.2.22](https://github.com/Niko1221/Strata/releases/tag/v0.2.22); its reports list each engine build |
| ROCm | 7.14.1 | tarball SHA-256 `c40e8f2bd6630a7d11557c762b99c6fa8afb04c9bd0e51ed1675ee1ca24afb00` (Owl's pin) |
| OS | Ubuntu 26.04.1 LTS, kernel 7.0.0-43-generic, linux-firmware 20260319.git217ca6e4 | |
| BIOS | EVO-X2S 1.13 (2026-06-26) | |
| GPU memory limit | `ttm pages_limit=29637703` (113 GiB) | |
| SSD | Crucial E100 2 TB (CT2000E100SSD8) | |

## Run it again

On the machine, stop all engines first. Each bench needs all of the memory.

```sh
sudo systemctl stop halogen maya strata

# halogen: the image's bench, then the prompt speed while it serves
podman run --rm --device /dev/kfd --device /dev/dri --group-add keep-groups --ipc=host --ulimit memlock=-1:-1 \
  -e HALOGEN_CHECKPOINT=/models/qwen38-flash-next-v2.hgn -e HALOGEN_WEIGHTS_LOCK=1 \
  -v ~/models/halogen:/models ghcr.io/peonist-ai/halogen-flash-server:0.20.7 bench
sudo systemctl start halogen && python3 halogen-prompt.py && sudo systemctl stop halogen

# Maya: one installed config per model; writes maya-bench.txt
cd ~/src/project-maya && ./maya.sh --bench --config .installed-<commit>-<hash>.json

# Strata: one saved preset per run
strata bench run --profile ~/.local/state/strata/launch/qwen.json --out ~/bench/strata-qwen

# Hash every model file
cd ~/models && find maya halogen strata -type f -size +1M -not -path '*/.cache/*' -print0 \
  | xargs -0 -P 8 -n 1 sha256sum > sha256sums.txt
```

Then make the SBOM on your computer: `uv run --no-project python -I docs/benchmarks/sbom.py docs/benchmarks/<date>`.
