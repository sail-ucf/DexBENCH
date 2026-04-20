# DexBENCH

DexBENCH is the public code and data release for the ACL 2026 main-conference paper on dual forward and backward reasoning over program execution.

## Repository Layout

- `src/preparation/`: builds runnable benchmark programs, collects coverage, and generates FOCC files.
- `src/api_callers/`: runs model queries for the main, CRISPE, ablation, RAP, and least-coverage studies.
- `src/evaluation/`: evaluates model outputs for forward and backward reasoning.
- `src/analysis/`: computes dataset statistics and summary tables.
- `src/experiments/`: contains auxiliary experiment scripts.
- `data/`: benchmark inputs, prompt templates, and CRUXEval utilities.
- `artifacts/`: generated local outputs; this directory is ignored by Git.

## Setup

Use Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in only the API keys needed for the experiments you plan to run.

## Data

The released data is under `data/`. Generated experiment outputs are intentionally ignored by Git. If you regenerate coverage metadata, the default output files are written under `artifacts/programs/`.

HumanEval and CRUXEval source files are included with upstream provenance and license notices in `THIRD_PARTY_NOTICES.md`. The raw PythonSaga JSONL file is not redistributed because the upstream pages do not state an explicit redistribution license. Download it from the original project if you need to rebuild from raw PythonSaga inputs.

Typical preparation order:

```bash
python src/preparation/benchmark_filtering_script.py
python src/preparation/coverage_collector.py
python src/preparation/focc_generator.py
```

Then run the desired API caller and matching evaluation script.

If anything appears missing or unclear, please open an issue. We are happy to improve the release.
