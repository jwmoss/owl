# Benchmarks

Each run is a benchmark of every engine and model on owl, a GMKtec EVO-X2 (Ryzen AI Max+ 395, 128 GB), at the
versions that `main` pins on that date. Each release attaches the newest run's three files.

| Run | Engines | Report | Raw output | SBOM |
|---|---|---|---|---|
| 2026-11-26 | halogen 0.20.7, Maya v1.1.81, Strata 0.2.22 | [2026-11-26.md](2026-11-26.md) | [2026-11-26.raw.txt](2026-11-26.raw.txt) | [2026-11-26.cdx.json](2026-11-26.cdx.json) |

## The three files of a run

| File | Holds |
|---|---|
| `<date>.md` | The results, how each bench measures, the models with their Hugging Face repo, commit and SHA-256, and the software versions |
| `<date>.raw.txt` | The raw output of every bench and long-prompt test, and the SHA-256 of every model file, one section each |
| `<date>.cdx.json` | A CycloneDX 1.6 SBOM: the machine, the engines and every model file, made by [sbom.py](sbom.py) |

## Search the results

```sh
rg -i deepseek docs/benchmarks/*.md                       # every DeepSeek result
rg -n '^=== ' docs/benchmarks/2026-11-26.raw.txt          # the sections of one raw file
jq -r '.components[] | select(.purl? // "" | test("GLM")) | .name' docs/benchmarks/2026-11-26.cdx.json
```

## Add a run

1. On the machine, stop all engines, then run each bench. The commands are in the newest run's report.
2. Hash every model file into a `sha256sums.txt`.
3. Put all the output into `<date>.raw.txt`, one `=== <name>` section each, with your home folder replaced by `~`.
4. Run `uv run --no-project python -I docs/benchmarks/sbom.py sha256sums.txt docs/benchmarks/<date>.cdx.json`.
5. Write `<date>.md`, and add a row to the table above.
6. Merge to `main`. The next release attaches the three files.
