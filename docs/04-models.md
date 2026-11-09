# 4. Inference engines and models

Each engine uses almost all of the 128 GB, so only one runs at a time.
Each engine is a systemd service, and the services conflict, so starting one stops the others.

| Service | Engine | Model | Port | Access | Playbook |
|---------|--------|-------|------|--------|----------|
| `strata` | [Strata](https://github.com/Niko1221/Strata) 0.2.12 | Qwen3.8-Flash-Next IQ3_S, 128K context | 8080 | LAN, API key | `strata.yml` |
| `gufo` | [gufo](https://github.com/gufo-org/gufo) 0.32.0 (Podman) | Qwen3.8-Flash-Next UD-Q4_K_XL + MTP | 8081 | localhost only | `gufo.yml` |
| `osmos` | [libosmos](https://github.com/mrsirg97-rgb/libosmos) | DeepSeek-V4.1-Flash-1017 UD-IQ1_M, abliterated | 8091 | localhost only | `libosmos.yml` |

`strata` starts at boot. To change that, set `default_engine` in `ansible/inventory/host_vars/owl.yml`.

## Switch engines

```sh
ssh jwmoss@192.168.1.241 sudo systemctl start osmos    # stops strata, starts DeepSeek
ssh jwmoss@192.168.1.241 sudo systemctl start strata   # back to Qwen
```

A large model takes some minutes to load. `GET /health` answers when it is ready.

## Use the APIs

All engines have an OpenAI-compatible `/v1/chat/completions`. Strata also has an Anthropic-compatible API.

Show the Strata API key on `owl`:

```sh
~/.local/bin/strata launch --show-key --preset qwen
```

`gufo` and `osmos` have no API key, so they listen on localhost only. Use an SSH tunnel:

```sh
ssh -N -L 8091:127.0.0.1:8091 jwmoss@192.168.1.241
```

## Model sources

All files come from Hugging Face. The engines pin the revisions, and Strata and libosmos check each file's SHA-256.

| Engine | Files | Repository |
|--------|-------|------------|
| Strata | Qwen3.8-Flash-Next IQ3_S (84 GB) | [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) |
| gufo | UD-Q4_K_XL, MTP head, picture reader (113 GB) | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) |
| libosmos | UD-IQ1_M and the Engram table (343 GB) | [unsloth/DeepSeek-V4.1-Flash-1017-GGUF](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) |
| libosmos | DSpark drafter, expert picks | [mrsirg97-rgb/osmos-evo-1017](https://huggingface.co/mrsirg97-rgb/osmos-evo-1017) |
| libosmos | Abliteration patch | [huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF) |

The files stay on the local NVMe disk. libosmos reads experts from the disk for each token with `O_DIRECT`,
so a network share does not work.

## Measured on owl

| Engine | Model | Decode | Date |
|--------|-------|--------|------|
| Strata | Qwen3.8-Flash-Next IQ3_S | 51.5 tok/s | 2026-11-08 |

Project Maya (DeepSeek-V4.1-Flash, can read the same unsloth files as libosmos) is next. It is not in the playbooks yet.
