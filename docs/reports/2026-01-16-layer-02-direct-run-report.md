# Layer 02 Direct LLM Run Report

## Summary
This report summarizes the execution of **Layer 02 (Naive and Optimized)** direct LLM runs performed on 2026-01-16. The Naive run was successfully completed after an initial configuration failure, while the Optimized run achieved a near-perfect completion rate (239/240) with one technical API failure.

## Run Details

### Naive Runs
| Run ID | Status | Completed | Failed | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `20260116_161315` | Failed | 0 | 160 | Initial run failed due to missing `ZENMUX_API_KEY`. |
| `20260116_191601` | Success | 18 | 0 | Partial recovery run. |
| `20260116_194321` | Success | 142 | 0 | Final recovery run completing the 160-question set. |
| **Total** | | **160** | **160** | **100% successful completion of recovery attempts.** |

### Optimized Run
| Run ID | Status | Completed | Failed | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `20260116_201510` | Success | 239 | 1 | Single failure due to upstream API gateway error. |

## Cost & Token Summary

### Aggregate Totals
| Configuration | Input Tokens | Output Tokens | Total Cost (USD) |
| :--- | :--- | :--- | :--- |
| **Naive (Successful)** | 5,709,220 | 34,756 | **$14.21** |
| **Optimized** | 8,702,056 | 83,629 | **$30.19** |

### Per-Model Stats (Optimized Run)
| Model | Completed | Failed | Input Tokens | Output Tokens | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `claude-opus-4-5` | 79 | 1 | 2,974,916 | 34,022 | $15.73 |
| `claude-sonnet-4-5` | 80 | 0 | 2,976,272 | 26,066 | $9.32 |
| `gpt-5.2` | 80 | 0 | 2,750,868 | 23,541 | $5.14 |

## Failures
Only one failure occurred during the successful run batches:
- **Run ID**: `20260116_201510` (Optimized)
- **Model**: `claude-opus-4-5`
- **Target**: Question `q12` on `investor_presentation.txt`
- **Error**: `502 Bad Gateway` from `https://opencode.ai/zen/v1/messages`
- **Impact**: One missing data point for Opus; Sonnet and GPT-5.2 completed this target successfully.

## Artifacts
All run events and responses are archived at the following locations:

- **Events (JSONL)**:
    - `results/wework-bowx/layers/02-direct/naive/events.jsonl`
    - `results/wework-bowx/layers/02-direct/optimized/events.jsonl`
- **Response Directories**:
    - `results/wework-bowx/layers/02-direct/naive/responses/20260116_191601`
    - `results/wework-bowx/layers/02-direct/naive/responses/20260116_194321`
    - `results/wework-bowx/layers/02-direct/optimized/responses/20260116_201510`
- **Input Data & Metadata**:
    - `experiments/wework-bowx/data/layer-02/*` (Prepared inputs)
    - `experiments/wework-bowx/data/layer-02/layer-02_meta.json` (Run metadata)

## Notes & Next Review Items
- **Metadata Caveat**: Analysis of `layer-02_meta.json` indicates that `section_coverage` resulted in a `coverage_ratio` of `0.0` for both the **S-4** and **investor_presentation** documents. In these cases, the system used the fallback slice for LLM context.
- **Quality Analysis**: The runs are ready for qualitative evaluation against the ground truth. No further reruns are planned despite the single Opus failure, as 239/240 samples provide sufficient statistical coverage for this layer.
