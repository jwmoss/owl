# 4. Inference engines and models

Each engine uses almost all of the 128 GB, so only one runs at a time.
Each engine is a systemd service, and the services conflict, so starting one stops the others.

| Service | Engine | Model | Port | Access | Playbook |
|---------|--------|-------|------|--------|----------|
| `strata` | [Strata](https://github.com/Niko1221/Strata) 0.2.12 | Qwen3.8-Flash-Next IQ3_S, 128K context | 8080 | LAN, API key | `strata.yml` |
| `gufo` | [gufo](https://github.com/gufo-org/gufo) 0.32.0 (Podman) | Qwen3.8-Flash-Next UD-Q4_K_XL + MTP | 8081 | LAN, no key | `gufo.yml` |
| `halogen` | [halogen](https://github.com/peonist-ai/halogen-flash-server) 0.20.0 (Podman, closed-source EULA) | Qwen3.8-Flash-Next halogen v2 (4.16 bpw) | 8731 | LAN, no key | `halogen.yml` |
| `osmos` | [libosmos](https://github.com/mrsirg97-rgb/libosmos) | DeepSeek-V4.1-Flash-1017 UD-IQ1_M, abliterated | 8091 | LAN, no key | `libosmos.yml` |
| `maya` | [Project Maya](https://github.com/mw00/project-maya) 1.1.56 | DeepSeek-V4.1-Flash-1017 Maya-XS | 8099 | LAN, no key | `maya.yml` |

`halogen` starts at boot. To change that, set `default_engine` in `ansible/inventory/host_vars/owl.yml`.

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

Only Strata has an API key. The other engines are open to the LAN without a key.

## Model sources

All files come from Hugging Face. The engines pin the revisions, and Strata and libosmos check each file's SHA-256.

| Engine | Files | Repository |
|--------|-------|------------|
| Strata | Qwen3.8-Flash-Next IQ3_S (84 GB) | [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) |
| gufo | UD-Q4_K_XL, MTP head, picture reader (113 GB) | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) |
| libosmos | UD-IQ1_M and the Engram table (343 GB) | [unsloth/DeepSeek-V4.1-Flash-1017-GGUF](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) |
| libosmos | DSpark drafter, expert picks | [mrsirg97-rgb/osmos-evo-1017](https://huggingface.co/mrsirg97-rgb/osmos-evo-1017) |
| libosmos | Abliteration patch | [huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF) |

| halogen | v2 checkpoint and lookup table (about 120 GB) | [peonist-ai/halogen-qwen3.8-flash-next](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next) |
| Maya | Maya-XS (about 277 GB) | [peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF](https://huggingface.co/peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF) |

The files stay on the local NVMe disk. libosmos reads experts from the disk for each token with `O_DIRECT`,
so a network share does not work.

## Measured on owl

| Engine | Model | Decode | Date |
|--------|-------|--------|------|
| Strata | Qwen3.8-Flash-Next IQ3_S | 51.5 tok/s | 2026-11-08 |

## Test

`ansible/test.yml` starts each engine, waits for its model, sends one chat request and checks the answer.

```sh
cd ansible
uvx --from ansible-core==2.22.0 ansible-playbook test.yml                          # all engines
uvx --from ansible-core==2.22.0 ansible-playbook test.yml -e '{"engines": ["strata"]}'
```

## Clients on the Mac

pi (`~/.pi/agent/models.json`) has one provider for each engine, `owl-<engine>`. The model names are
`owl-<engine>-<model>-<quant>[-<variant>]`, for example `owl-gufo-qwen3.8-flash-next-ud-q4_k_xl`.
`enabledModels` in `~/.pi/agent/settings.json` sets the Ctrl+P order: the Qwen engines, then DeepSeek.

`owl` in `~/.zshrc` switches engines:

```sh
owl use gufo     # start gufo, stop the others, wait until the model is loaded
owl status       # show which engine runs
```
