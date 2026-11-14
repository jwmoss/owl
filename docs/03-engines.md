# 3. Inference engines and models

Each engine uses almost all of the 128 GB, so only one runs at a time.
Each engine is a systemd service, and the services conflict, so starting one stops the others.

| Service | Engine | Model | Port | Access | Playbook |
|---------|--------|-------|------|--------|----------|
| `strata` | [Strata](https://github.com/Niko1221/Strata) | Qwen3.8-Flash-Next IQ3_S, 128K context, or another preset (`strata_preset`) | 8080 | LAN, API key | `strata.yml` |
| `gufo` | [gufo](https://github.com/gufo-org/gufo) (Podman) | Qwen3.8-Flash-Next UD-Q4_K_XL + MTP, or the abliterated v2 (`gufo_abliterated`) | 8081 | LAN, no key | `gufo.yml` |
| `halogen` | [halogen](https://github.com/peonist-ai/halogen-flash-server) (Podman, closed-source EULA) | Qwen3.8-Flash-Next halogen v2 (4.16 bpw), or the abliterated r2 (`halogen_abliterated`) | 8731 | LAN, no key | `halogen.yml` |
| `maya` | [Project Maya](https://github.com/mw00/project-maya) | DeepSeek-V4.1-Flash-1017 Maya-XS, or another model (`maya_model`) | 8099 | LAN, no key | `maya.yml` |

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
| [Strata](https://github.com/Niko1221/Strata/blob/v0.2.13/README.md#models) | Qwen3.6-35B-A3B; other Qwen Flash quants; DeepSeek-V4.1-Flash | `strata_presets` lists the models to set up. Read [Swap models](#swap-models). |
| [gufo](https://github.com/gufo-org/gufo/blob/v0.33.0/README.md#models) | Qwen3.8-27B, DeepSeek V4 Flash, embeddings, speech, images and video | The role configures Qwen Flash only. |
| [Maya](https://github.com/mw00/project-maya/blob/v1.1.58/docs/MODELS.md) | GLM-5.3-Flash, full GLM-5.3, MiniMax-M3.1-Flash and Qwen Flash | `maya_models` lists the models to set up. Read [Swap models](#swap-models). |
| [halogen](https://github.com/peonist-ai/halogen-flash-server/blob/v0.20.1/docs/NPU.md) | Small classifiers, embeddings, rerankers, moderation and other NPU models | `halogen_npu_models` selects the NPU models beside Qwen Flash. |

Do not treat upstream support as a successful test on this machine. Additional model families need Ansible download, launch and test support.
An engine update does not change Owl's selected model family. An environment override does not replace the role's download and launch configuration.

## Swap models

Maya and Strata set up every model in their list and serve one of them.
Set the lists and the served model in `ansible/inventory/group_vars/all.yml`:

| Engine | Models, by name | Model it serves | Model files |
|--------|-----------------|-----------------|-------------|
| Maya | `maya_models` | `maya_model` | `~/models/maya`, passed as `--models-dir` |
| Strata | `strata_presets` | `strata_preset` | `~/models/strata`, passed as `STRATA_DATA_DIR` |

Swap the served model with one command. If the engine runs, the playbook restarts it with the new model.

```sh
ansible-playbook maya.yml -e maya_model=glm
ansible-playbook strata.yml -e strata_preset=<name>
```

Each model can have an `env` map. The service gets `maya_env` or `strata_env`, then the served model's `env`:

```yaml
maya_models:
  glm: { model: glm-maya-s, env: { NAME: "value" } }
```

To keep a swap, change `maya_model` or `strata_preset` in `all.yml`.
The Strata API key is per preset: `~/.local/bin/strata launch --show-key --preset <preset>`.

### Model files and the model store

Every engine keeps its files in `models_dir/<engine>` (`~/models/halogen`, `~/models/maya` ...), set with the engine's
own option: `--local-dir`, `--models-dir`, `--models` or `STRATA_DATA_DIR`. Hugging Face's own cache
(`~/.cache/huggingface/hub`) is not used: each engine downloads into its own layout and builds index files beside it.

The model store is optional. Set `model_cache_nfs` to an NFS share in your host_vars, for example
`<nas-ip>:/mnt/user/huggingface`, or a Tailscale name such as `tower:/mnt/user/huggingface` after `tailscale.yml`.
The playbooks mount it at `/mnt/model-cache` and keep the files in `owl/<engine>` on the share.
Each file then downloads from Hugging Face once, and a fresh machine gets its models from the share.

- halogen and gufo copy their files from the share before the download, and save them to the share after.
- Maya and Strata keep each model in `owl/maya/<name>` and `owl/strata/<name>`, and only the served one on the SSD.
  A swap stops the engine, makes the SSD match the new model's folder on the share, and starts the engine.
- To keep more models on the SSD for fast swaps, name them in `model_cache_keep`, for example
  `model_cache_keep: [deepseek, glm-derisked]`.
- The `.done` file marks a complete copy. A Maya or Strata model without it is set up again: the engine downloads
  only missing files.
- The engines always run from the SSD: over 1 Gbps a model loads too slowly to run from the share.
  A copy of 100 GB takes about 15 minutes on the LAN and about 30 minutes over Tailscale.

### Maya models

"On owl" is the [VRAM Calculator](https://vramcalculator.com/project-maya-calculator/?fam=glm&unified=strix-halo-395-128&ram=128&ctx=262144&os=linux)'s
estimate at 256K context, not a measurement. Owl tests only `deepseek-maya-xs`.
Every model reads pictures: the setup gets the model's vision encoder (about 1.1 GB).

| Model | `model` | On owl |
|-------|---------|--------|
| DeepSeek-V4.1-Flash-1017 | `deepseek-maya-xs` (`deepseek`, the default) | Runs from memory |
| DeepSeek-V4.1-Flash-1017 | `deepseek-maya-s`, `deepseek-maya-m` | Reads experts from SSD |
| DeepSeek-V4.1-Flash-1017, orcarouter's abliterated build (gated: accept its terms on Hugging Face) | `DeepSeek-V4.1-Flash-1017 --ds4-quant abliterated-128g` | Runs from memory |
| GLM-5.3-Flash | `glm-maya-xs`, `glm-maya-s` (`glm`), `glm-maya-s24` | Runs from memory |
| GLM-5.3-Flash | `glm-maya-m`, `glm-maya-m-derisked`, `glm-maya-l`, `EXL3-3.05bpw`, `EXL3-4.05bpw`, `EXL3-sc_4.10bpw` | Reads experts from SSD |
| GLM-5.3 (744B) | `GLM-5.3-Maya-XS`, `GLM-5.3-UD-IQ2_M` | Reads experts from SSD |
| MiniMax-M3.1-Flash (non-commercial license) | `minimax-maya-xs` (`minimax`) | Runs from memory |
| MiniMax-M3.1-Flash (non-commercial license) | `minimax-maya-s` | Reads experts from SSD |
| Qwen-3.8-Flash-Next | `cyber-frost`, `qwen-ud-iq2_xs` | Runs from memory |

A model's `model` holds all the `--model` options of `maya.sh`. For DeepSeek's unsloth and EXL3 files, set `model` to a value such as
`DeepSeek-V4.1-Flash-1017 --ds4-quant gguf-iq1_s`. `./maya.sh --help` lists the `--ds4-quant`, `--mm3-quant` and `--qwen-quant` values.

### Strata presets

Each `strata_presets` item names a `--family` and a `--model` of `strata launch`, and optionally a `context` and an `env`.
Run `~/.local/bin/strata launch --model x --plan` on the machine to list the model names.
Every preset reads pictures: the setup passes `--vision gpu`, so Strata gets each model's picture reader.

| Preset | Model | Download |
|--------|-------|----------|
| `qwen` (default) | Qwen3.8-Flash-Next IQ3_S | 84 GB |

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
ssh <user>@<host> sudo systemctl start maya      # stops the running engine, starts the Maya model
ssh <user>@<host> sudo systemctl start halogen   # back to Qwen
```

A large model takes some minutes to load. `GET /health` answers when it is ready.
Each service waits until about 100 GiB is free, because the GPU driver frees the last engine's memory some seconds after it stops.

Follow an engine's log: `ssh <user>@<host> journalctl -u halogen -f`.

## Use the APIs

All engines have an OpenAI-compatible `/v1/chat/completions`. Strata also has an Anthropic-compatible API.

Show the Strata API key on the server:

```sh
~/.local/bin/strata launch --show-key --preset qwen  # or another preset
```

## Model sources

All files come from Hugging Face. The engines pin the revisions, and Strata and Maya check each file's SHA-256.

| Engine | Files | Repository |
|--------|-------|------------|
| Strata | Qwen3.8-Flash-Next IQ3_S (84 GB) | [ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF) |
| gufo | UD-Q4_K_XL, MTP head, picture reader (113 GB) | [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) |
| gufo (`gufo_abliterated: true`) | Abliterated UD-Q4_K_XL v2 (112 GB) | [huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF) |
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
- It lets halogen fetch the NPU models (a few GB) into `~/models/halogen/npu` on its first start.

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
