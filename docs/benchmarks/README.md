# Benchmarks

Each folder is one benchmark run on owl, a GMKtec EVO-X2 (Ryzen AI Max+ 395, 128 GB). A run uses each engine's own
bench, at the versions that `main` pins on that date.

| Run | Engines | Record | Results | SBOMs |
|---|---|---|---|---|
| 2026-11-26 | halogen 0.20.7, Maya v1.1.81, Strata 0.2.22 | [README](2026-11-26/README.md) | [results.csv](2026-11-26/results.csv) | [CycloneDX](2026-11-26/sbom.cdx.json) · [SPDX](2026-11-26/sbom.spdx.json) |

## Each run folder holds

| File | Holds |
|---|---|
| `README.md` | The results, the models with their Hugging Face repo, commit and SHA-256, the software versions, and how to run it again |
| `results.csv` | One row per model: engine, version, Hugging Face repo and commit, quant, context, decode and prompt speed |
| `sha256sums.txt` | The SHA-256 of every model file, hashed on the machine |
| `sbom.cdx.json`, `sbom.spdx.json` | The same list as CycloneDX 1.6 and SPDX 2.3, made by [sbom.py](sbom.py) |
| `halogen-*.txt`, `maya-*.txt`, `strata-*/` | The raw output of each bench |

## Search the results

```sh
rg -i deepseek docs/benchmarks/*/results.csv                # every DeepSeek row, in all runs
rg 1.1.81 docs/benchmarks/*/results.csv                      # every row for one engine version
rg 4c1eb2ceb4915e11 docs/benchmarks/*/sha256sums.txt         # which file has this SHA-256
jq -r '.components[] | select(.purl? // "" | test("GLM")) | .name' docs/benchmarks/2026-11-26/sbom.cdx.json
```

## Add a run

1. Stop all engines, then run each bench. The commands are in the latest run's README.
2. Hash every model file into `sha256sums.txt`.
3. Copy the raw output into a new folder `<date>/`, and replace your home folder in the paths with `~`.
4. Run `uv run --no-project python -I docs/benchmarks/sbom.py docs/benchmarks/<date>` for the SBOMs.
5. Write `README.md` and `results.csv`, and add a row to the table above.
