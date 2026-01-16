# How to Run Layer 02 (Direct LLM)

## 1. Setup Data

Ensure the data preparation script has run:
```bash
.venv/bin/python scripts/prep_layer_02.py
```
This creates `experiments/wework-bowx/data/layer-02/s4_risk_factors.txt` and `investor_presentation.txt`.

The prep step applies a deterministic, section-priority truncation protocol so every model
sees the same bounded slice of the S-4 and investor deck. It also writes a
`experiments/wework-bowx/data/layer-02/layer-02_meta.json` metadata sidecar with
budget, hash, and section-coverage details for reproducibility. The investor presentation
source must be the real deck text (no placeholders).

## 2. Run Experiments

**Option A: Run Naive Baseline (160 tasks)**
```bash
.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config_naive.yaml
```

**Option B: Run Optimized Experiment (240 tasks)**
```bash
.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config.yaml
```

## 3. Monitor Status

Check completion:
```bash
.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config.yaml --status
```

## 4. Run on Server (Headless)

Use `nohup` to prevent timeouts:
```bash
nohup .venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config.yaml > run_opt.log 2>&1 &
tail -f run_opt.log
```
