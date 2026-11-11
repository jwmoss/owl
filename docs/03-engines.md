# 3. Inference engines and models

Each engine uses almost all of the 128 GB, so only one runs at a time.
Each engine is a systemd service, and the services conflict, so starting one stops the others.

| Service | Engine | Model | Port | Access | Playbook |
|---------|--------|-------|------|--------|----------|
| `strata` | [Strata](https://github.com/Niko1221/Strata) | Qwen3.8-Flash-Next IQ3_S, 128K context | 8080 | LAN, API key | `strata.yml` |
| `gufo` | [gufo](https://github.com/gufo-org/gufo) (Podman) | Qwen3.8-Flash-Next UD-Q4_K_XL + MTP, or the abliterated v2 (`gufo_abliterated`) | 8081 | LAN, no key | `gufo.yml` |
| `halogen` | [halogen](https://github.com/peonist-ai/halogen-flash-server) (Podman, closed-source EULA) | Qwen3.8-Flash-Next halogen v2 (4.16 bpw), or the abliterated r2 (`halogen_abliterated`) | 8731 | LAN, no key | `halogen.yml` |
| `osmos` | [libosmos](https://github.com/mrsirg97-rgb/libosmos) | DeepSeek-V4.1-Flash-1017 UD-IQ1_M, abliterated | 8091 | LAN, no key | `libosmos.yml` |
| `maya` | [Project Maya](https://github.com/mw00/project-maya) | DeepSeek-V4.1-Flash-1017 Maya-XS | 8099 | LAN, no key | `maya.yml` |

The table shows Owl's configured models. Read [group_vars/all.yml](../ansible/inventory/group_vars/all.yml) for the exact engine versions and model revisions.

`halogen` starts at boot. To change that, set `default_engine` in `ansible/inventory/group_vars/all.yml`.

Only Strata has an API key. The other engines are open to your network without a key, so run them only on a trusted network.

Maya reserves 16 GiB of GPU memory on this machine. The 1 GiB upstream default can fail during model load.
Set `maya_vram_reserve_mib` to change this reserve. Setup skips the optional speed calibration.

## Other models and memory limits

An engine can support more models than its Owl role configures. These are separate choices:

- The engine version controls which model formats and features the software supports.
- The model files control the base model, quantization and any abliteration.
- The Ansible role controls which files to download and which model the service starts.

These examples come from the upstream versions linked below. They do not list every supported model.

| Engine | Additional upstream choices | Owl configuration |
|--------|-----------------------------|-------------------|
| [Strata](https://github.com/Niko1221/Strata/blob/v0.2.13/README.md#models) | Qwen3.6-35B-A3B; other Qwen Flash quants | The role fixes the family to Qwen Flash. `strata_model` selects its quant. |
| [libosmos](https://github.com/mrsirg97-rgb/libosmos/blob/v0.6.1/README.md#the-packs) | Qwen3.8-Flash-Next packs | `libosmos_pack` selects the pack. Owl tests the default DeepSeek pack. |
| [gufo](https://github.com/gufo-org/gufo/blob/v0.33.0/README.md#models) | Qwen3.8-27B, DeepSeek V4 Flash, embeddings, speech, images and video | The role configures Qwen Flash only. |
| [Maya](https://github.com/mw00/project-maya/blob/v1.1.58/docs/MODELS.md) | GLM-5.3-Flash, full GLM-5.3, MiniMax-M3.1-Flash and Qwen Flash | The role fixes the model to `deepseek-maya-xs`. |
| [halogen](https://github.com/peonist-ai/halogen-flash-server/blob/v0.20.1/docs/NPU.md) | Small classifiers, embeddings, rerankers, moderation and other NPU models | `halogen_npu_models` selects the NPU models beside Qwen Flash. |

Do not treat upstream support as a successful test on this machine. Additional model families need Ansible download, launch and test support.
An engine update does not change Owl's selected model family. An environment override does not replace the role's download and launch configuration.

Maya's [memory guide](https://github.com/mw00/project-maya/blob/v1.1.58/docs/MEMORY.md) lists these options.
The memory figures are upstream recommendations at the documented context, not results from Owl tests.

| Model and quant | Download | Recommended memory | On a 128 GB Strix Halo |
|-----------------|----------|--------------------|-----------------------|
| GLM-5.3-Flash Maya-XS | 73 GB | 88 GB | Fits by the upstream guide; not tested by Owl |
| GLM-5.3-Flash Maya-S | 97 GB | 128 GB | Upstream lists 128 GB; not tested by Owl |
| MiniMax-M3.1-Flash Maya-XS | 93 GB | 128 GB | Upstream lists 128 GB; not tested by Owl |
| Full GLM-5.3 Maya-XS | 170 GB | 192 GB | Some experts must come from SSD; not tested by Owl |

Strix Halo shares memory between the CPU and GPU. Count that memory once.
Download size is not the memory requirement. DeepSeek's download includes n-gram tables that stay on SSD.
Longer contexts need more memory. Run only one large engine at a time.

## Switch engines

```sh
ssh <user>@<host> sudo systemctl start osmos     # stops the running engine, starts DeepSeek
ssh <user>@<host> sudo systemctl start halogen   # back to Qwen
```

A large model takes some minutes to load. `GET /health` answers when it is ready.
Each service waits until about 100 GiB is free, because the GPU driver frees the last engine's memory some seconds after it stops.

Follow an engine's log: `ssh <user>@<host> journalctl -u halogen -f`.

## Use the APIs

All engines have an OpenAI-compatible `/v1/chat/completions`. Strata also has an Anthropic-compatible API.

Show the Strata API key on the server:

```sh
~/.local/bin/strata launch --show-key --preset qwen
```

## Model sources

All files come from Hugging Face. The engines pin the revisions, and Strata and libosmos check each file's SHA-256.

| Engine | Files | Repository |
|--------|-------|------------|
| Strata | Qwen3.8-Flash-Next IQ3_S (84 GB) | [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) |
| gufo | UD-Q4_K_XL, MTP head, picture reader (113 GB) | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) |
| gufo (`gufo_abliterated: true`) | Abliterated UD-Q4_K_XL v2 (112 GB) | [huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF) |
| libosmos | UD-IQ1_M and the Engram table (343 GB) | [unsloth/DeepSeek-V4.1-Flash-1017-GGUF](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF) |
| libosmos | DSpark drafter, expert picks | [mrsirg97-rgb/osmos-evo-1017](https://huggingface.co/mrsirg97-rgb/osmos-evo-1017) |
| libosmos | Abliteration patch | [huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4.1-Flash-1017-abliterated-GGUF) |
| halogen | v2 checkpoint and lookup table (about 120 GB) | [peonist-ai/halogen-qwen3.8-flash-next](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next) |
| halogen (`halogen_abliterated: true`) | Abliterated r2 checkpoint (about 89 GB) | [Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated](https://huggingface.co/Quat3rnion/halogen-qwen3.8-flash-next-v2-abliterated) |
| Maya | Maya-XS (about 277 GB) | [peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF](https://huggingface.co/peasantsmith/DeepSeek-V4.1-Flash-1017-Maya-GGUF) |

Set `halogen_abliterated: true` to serve the uncensored build from halogen: the stock v2 checkpoint
with the refusal direction from orcarouter's uncensored fine-tune transplanted into 149 tensors.
Speed and memory stay the same. The playbook pins the r2 revision, the one validated against the
stock lookup table and tokenizer, and checks the file's SHA-256.

### halogen on the NPU

halogen can serve small models on the NPU beside the Flash model on the GPU, on the same port.
Name them in `halogen_npu_models`, for example `decider-0.8b,qwen3-embedding-0.6b,qwen3-reranker-0.6b,qwen3guard-gen-0.6b,qwen3.5-2b`.
The request's `model` picks the NPU model, on `/v1/embeddings`, `/v1/rerank`, `/v1/systemone` and the others.
[halogen's NPU page](https://peonist.ai/halogen/docs/NPU/) lists the models and the request shapes.

The playbook then does three things:

- It passes `/dev/accel/accel0` to the container.
- It installs halogen's `halogen-fabric-clock` unit. GPU and NPU work at once can hang Strix Halo unless the GPU
  fabric clock is held ([ROCm/TheRock#8709](https://github.com/ROCm/TheRock/issues/8709)).
  The hold costs about 1 W. Install your vendor's newest BIOS too.
- It lets halogen fetch the NPU models (a few GB) into `~/Models/halogen/npu` on its first start.

The NPU models use about 8 GiB of memory more, and the Flash model is a little slower while the NPU works.

### Engine settings

Each engine has an `<engine>_env` setting, for example `halogen_env` or `gufo_env`. Its entries go to the engine
as environment variables, with `-e` for a container and `Environment=` for a host service. For halogen, use the names in
[halogen's flags](https://peonist.ai/halogen/docs/FLAGS/):

```yaml
# ansible/inventory/host_vars/<host>.yml
halogen_env:
  HALOGEN_WEIGHTS_LOCK: "1" # keep the Flash model in memory while NPU models work
```

The files stay on the local NVMe disk. libosmos reads experts from the disk for each token with `O_DIRECT`,
so a network share does not work.

## Measured on a GMKtec EVO-X2 (128 GB)

| Engine | Model | Decode | Date |
|--------|-------|--------|------|
| Strata | Qwen3.8-Flash-Next IQ3_S | 51.5 tok/s | 2026-11-08 |

## Test

`ansible/test.yml` starts each installed engine, waits for its model, sends one chat request and checks the answer.
It fails if no requested engine is installed. It starts the default engine again after a test failure.
For halogen, it also checks that each configured NPU model appears with the NPU backend.
It sends requests to configured `decider-0.8b`, `qwen3-embedding-0.6b`, `qwen3-reranker-0.6b`, `qwen3guard-gen-0.6b` and `qwen3.5-2b` models.
Other NPU models get the backend check only.

```sh
cd ansible
ansible-playbook test.yml                                # all engines that you installed
ansible-playbook test.yml -e '{"engines": ["halogen"]}'
```

## Use with pi

[pi](https://github.com/earendil-works/pi) can use each engine as a provider. Add the engine to `~/.pi/agent/models.json`.
This example is for halogen. The `id` must match the engine's `GET /v1/models`:

```json
{
  "providers": {
    "owl-halogen": {
      "baseUrl": "http://<host>:8731/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [
        {
          "id": "halogen-qwen3.8-flash-next",
          "name": "owl-halogen-qwen3.8-flash-next-4.16bpw",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 262144,
          "maxTokens": 32768
        }
      ]
    }
  }
}
```

Start pi with `<provider>/<model id>`. Add `:low` for less thinking (halogen defaults to `xhigh`):

```sh
pi --model owl-halogen/halogen-qwen3.8-flash-next
pi --model owl-halogen/halogen-qwen3.8-flash-next -p "What is 17 times 3?"   # one answer, then exit
```

A shorter system prompt makes the first answer faster. These flags remove parts of it:

| Flag | Removes |
|------|---------|
| `-ns` | skills |
| `-nc` | AGENTS.md and CLAUDE.md |
| `-ne` | extensions |
| `--no-mcp` | MCP servers and their tools |
| `-np` | prompt templates |
| `-nt` | all tools (plain chat) |

```sh
pi --model owl-halogen/halogen-qwen3.8-flash-next -ns -nc -ne --no-mcp -np
```
