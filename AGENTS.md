# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-07
**Branch:** main

## OVERVIEW

AI-human symbiosis research for deal analysis. Tests 21 experimental layers against WeWork/BowX SPAC merger (2021 to bankruptcy 2023) to measure what AI catches vs. misses. Python 3.11+, LLM APIs via ZenMux (94 models), research-centric structure.

## STRUCTURE

```
DealSignals/
├── dealsignals/                   # Main Python package
│   ├── core/                      # Core types and config
│   │   ├── types.py               # Question, CompletionResponse, RunEvent
│   │   └── config.py              # Global config, API keys
│   ├── providers/                 # LLM provider integrations
│   │   ├── base.py                # Abstract Provider interface
│   │   ├── zenmux.py              # ZenMux (94 models via Zen API)
│   │   └── registry.py            # Model aliases (claude -> anthropic/claude-opus-4.5)
│   ├── questions/                 # Question management
│   │   ├── bank.py                # QuestionBank with filtering
│   │   └── loader.py              # YAML question loader
│   ├── experiment/                # Experiment orchestration
│   │   ├── definition.py          # ExperimentDefinition from YAML
│   │   ├── state.py               # JSONL-based state tracking
│   │   └── runner.py              # ExperimentRunner with callbacks
│   ├── evaluation/                # Scoring (placeholder)
│   ├── output/                    # Output formatting (placeholder)
│   └── cli/                       # CLI commands
├── experiments/                   # Experiment definitions
│   └── wework-bowx/
│       ├── config.yaml            # Case study config
│       ├── ground-truth/          # LOCKED before AI testing
│       │   ├── questions.yaml     # 40 eval questions
│       │   ├── answers.yaml       # Expert answers template
│       │   └── Human_gt_q1_q10.md # Completed Q1-Q10
│       ├── layers/                # Each layer = self-contained research
│       │   ├── 01-contamination/
│       │   │   ├── config.yaml    # Layer config
│       │   │   └── prompts/       # system.md, user.md
│       │   └── ...                # Layers 02-21 per Methodology.md
│       └── data/                  # SEC filings (gitignored, 429MB)
├── scripts/                       # CLI runner scripts
│   └── run.py
├── journal/                       # Build-in-public logs
├── Methodology.md                 # Full 21-layer research design
└── pyproject.toml                 # Package config with CLI entry point
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Run LLM calls | `dealsignals/providers/zenmux.py` | ZenMux provider, 94 models |
| Model aliases | `dealsignals/providers/registry.py` | `claude` -> `anthropic/claude-opus-4.5` |
| Core types | `dealsignals/core/types.py` | Question, CompletionResponse, RunEvent |
| Load questions | `dealsignals/questions/loader.py` | YAML -> Question objects |
| Filter questions | `dealsignals/questions/bank.py` | By tag, difficulty, range |
| Run experiments | `dealsignals/experiment/runner.py` | ExperimentRunner with progress |
| Experiment config | `dealsignals/experiment/definition.py` | Load from YAML |
| Track state | `dealsignals/experiment/state.py` | JSONL-based, resume support |
| CLI commands | `dealsignals/cli/__init__.py` | run, status, models |
| Research methodology | `Methodology.md` | 21 layers, evaluation criteria |
| Ground truth | `experiments/wework-bowx/ground-truth/` | Q1-Q10 done, Q11-Q40 pending |
| Layer configs | `experiments/wework-bowx/layers/*/config.yaml` | Declarative experiment definitions |
| Layer prompts | `experiments/wework-bowx/layers/*/prompts/` | Version-controlled prompts |

## CONVENTIONS

| Rule | Detail |
|------|--------|
| Line length | 100 (Ruff) |
| Linting | Ruff rules E, F, I, W |
| Python | 3.11+ required |
| Dependencies | Optional groups: `llm`, `parsing`, `rag`, `dev` |
| Structure | Experiments in YAML configs, prompts in markdown files |
| Ground truth | LOCK answers before AI testing. Never revise based on AI results |
| State tracking | JSONL files for pause/resume support |

## ANTI-PATTERNS (THIS PROJECT)

| Never | Why |
|-------|-----|
| Commit API keys | Pre-commit hook blocks anthropic/openai key patterns |
| Modify ground-truth after AI runs | Contaminates evaluation |
| Hardcode prompts in Python | Use `prompts/*.md` for version control |
| Run experiments without venv | Dependencies isolated in `.venv/` |
| Commit SEC data | Gitignored, 429MB, re-downloadable from EDGAR |

## UNIQUE STYLES

- **Declarative experiments**: YAML configs define what to run, prompts in markdown
- **State as JSONL**: Each line is an event, easy to resume/replay
- **Model registry**: Aliases map friendly names to provider/model paths
- **Contamination controls**: Layer 01 tests what LLMs "know" before seeing documents
- **Failure mode taxonomy**: 8 error types (extraction, calculation, reasoning, omission, hallucination, contamination, relevance, confidence)
- **Citation requirements**: Every AI claim must cite document + page + quote

## COMMANDS

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[all,dev]"

# Run experiment (CLI)
ds run --config experiments/wework-bowx/layers/01-contamination/config.yaml --models claude gpt4

# Check status
ds status --config experiments/wework-bowx/layers/01-contamination/config.yaml

# List available models
ds models

# Run directly with script
python scripts/run.py --config experiments/wework-bowx/layers/01-contamination/config.yaml --dry-run

# Lint
ruff check .
ruff format .
```

## NOTES

- **Current state**: Full refactor complete. New `dealsignals/` package replaces old `lib/`
- **ZenMux integration**: 94 models via single API (Zen)
- **Ground truth progress**: Q1-Q10 completed by human expert, Q11-Q40 pending
- **Data location**: SEC filings in `experiments/wework-bowx/data/` (gitignored)
- **iCloud sync**: Project on iCloud Drive, git operations can be slow
- **TODO tracking**: `TODO.local.md` for local tasks (gitignored)
