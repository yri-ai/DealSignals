# Layer 02 Direct LLM Fairness Design

**Goal:** Make Layer 02 “Direct LLM” fair and usable despite context window limits, while preserving its no-retrieval baseline.

**Problem:** Current Layer 02 only uses a narrow slice of the documents (risk factors + investor deck, with a placeholder), which makes the baseline unfair and misaligned with the methodology’s intent for direct LLM capability.

## Chosen Approach (Option A)
**Section-priority truncation** with deterministic budgets and optional window rotation. No retrieval and no LLM summarization. The model receives a deterministic, best-effort slice of the full documents within a fixed budget.

## Truncation Protocol
- **Fixed budget per document** (example starting point):
  - S-4: 80k tokens
  - Investor presentation: 40k tokens
- **Deterministic section ordering** (S-4 example):
  1. Risk Factors
  2. Summary
  3. Selected Financial Data
  4. Management’s Discussion & Analysis
  5. Projections
  6. Transaction Terms
  7. Related-Party / Conflicts
  8. Legal / Regulatory
  9. Appendices
- **Investor deck ordering**:
  1. Executive Summary
  2. Market / Strategy
  3. Unit Economics
  4. Financial Projections
  5. Risks / Disclaimers
- **Selection rule**: include sections in order until the budget is exhausted.
- **Optional rotation**: alternate “Risk-first” vs “Financials-first” ordering across runs to measure truncation sensitivity.

## Pipeline & Artifacts
- **Inputs**
  - Full S-4 text (`experiments/wework-bowx/data/merger/.../2021-09-17_d166510ds4a.txt`)
  - Full investor presentation text (real file, no placeholders)
- **Preprocessing output**
  - `experiments/wework-bowx/data/layer-02/s4_risk_factors.txt` (now a deterministic truncated slice, not just risk factors)
  - `experiments/wework-bowx/data/layer-02/investor_presentation.txt` (truncated, real content)
  - `experiments/wework-bowx/data/layer-02/layer-02_meta.json` (truncation metadata)
- **Metadata fields**
  - Source file hashes
  - Section ordering and offsets
  - Total chars and estimated tokens
  - Budget used, rotation mode

## Evaluation & Fairness Checks
- All models receive identical truncated inputs.
- Truncation metadata is included with each run for auditability.
- Basic coverage diagnostics (keyword presence) explain “Not found” outcomes.
- Version truncation protocol when it changes (e.g., `layer-02-direct-v2`).

## Validation
- Preprocessor asserts input files exist (no placeholders).
- Output files must be non-empty and within budget.
- Missing section headers trigger a deterministic fallback slice plus warnings.

## Open Questions
- Confirm token budgets per document (start with 80k/40k or adjust).
- Finalize section header patterns for S-4 and investor deck.
- Decide whether to enable rotation by default.

## Next Steps
1. Update `scripts/prep_layer_02.py` to implement section parsing + deterministic truncation + metadata output.
2. Replace investor presentation placeholder with actual text source.
3. Update `experiments/wework-bowx/layers/02-direct/README.md` to document the truncation protocol.
4. Run Layer 02 naive + optimized with the new prepared inputs.
