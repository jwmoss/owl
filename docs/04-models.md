# 4. Inference engines and models

Run one engine at a time. Each engine uses almost all of the 128 GB.

## Plan

| Use | Engine | Model | Disk |
|-----|--------|-------|------|
| Daily chat and coding agents | [Strata](https://github.com/Niko1221/Strata) | Qwen3.8-Flash-Next (IQ3_S or IQ3_XXS) | about 80 GB |
| Largest model | [libosmos](https://github.com/mrsirg97-rgb/libosmos) | DeepSeek-V4.1-Flash-1017 `ud-iq1_m`, optional `--abliterated` | about 345 GB |
| Backup DeepSeek engine | [Project Maya](https://github.com/mw00/project-maya) | DeepSeek-V4.1-Flash-1017 | — |

## Strata

- OpenAI- and Anthropic-compatible API. `strata connect` shows the setup for Claude Code, Codex and OpenCode.
- On Strix Halo, Strata runs DeepSeek only on **Windows**. On Linux, use it for Qwen.

## libosmos

- Built for one Strix Halo with 128 GB. The dense weights stay in GPU memory.
  The routed experts that do not fit are read from the NVMe disk for each token.
- Needs ROCm 7.x at `/opt/rocm`, about 113 GiB of GPU memory through `ttm`, and an ext4, btrfs or xfs disk.
- Install and serve (OpenAI-compatible API on port 8091):

  ```sh
  git clone https://github.com/mrsirg97-rgb/libosmos && cd libosmos
  python3 tools/install/osmos_install.py ud-iq1_m --abliterated --serve
  ```

- The developer reports 35–43 tok/s with drafting and 17–20 tok/s without.
  The Crucial E100 is a budget disk, so DeepSeek can be slower on `owl`.

## Other models that fit on one 128 GB Strix Halo

Reported on X, October–November 2026. These numbers are not checked.

| Model | Notes |
|-------|-------|
| Qwen3.8-Flash-Next | 40–60 tok/s in Strata, TensorFold or Halogen; about 20 in Ollama |
| Qwen3.8-27B (dense) | About 8–10 tok/s at Q8 |
| Qwen3.6-35B-A3B | Fast everyday model |
| LFM2.5-24B-A2B | About 114 tok/s, made for agents |
| gpt-oss-120b | Fast MoE |
| GLM-5.3 Flash | Custom quants only, experimental |

Too large for one 128 GB box: MiniMax M3.1 Flash, Mistral Large 4, Kimi K2.6.
