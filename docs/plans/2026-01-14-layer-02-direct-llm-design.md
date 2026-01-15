# Layer 02: Direct LLM Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement Layer 02 (Direct LLM Baseline) to test raw model capability on fitting documents (Investor Presentation + S-4 Risk Factors) using both naive and optimized prompts.

**Architecture:**
- **Data Prep:** Extract "Risk Factors" section from S-4/A to create a fitting document. Convert Investor Presentation to text.
- **Config:** Create `experiments/wework-bowx/layers/02-direct/config.yaml` defining the 2 sub-layers (Naive vs. Optimized) as variants or separate runs.
- **Prompts:** Create naive ("Answer this") and optimized ("Role: Analyst... Cite sources") prompts.
- **Runner:** Use existing `scripts/run.py` which supports document loading.

**Tech Stack:** Python 3.11+, PyYAML, `dealsignals` package.

---

### Task 1: Data Preparation Script

**Files:**
- Create: `scripts/prep_layer_02.py`
- Create: `experiments/wework-bowx/data/layer-02/s4_risk_factors.txt` (output)
- Create: `experiments/wework-bowx/data/layer-02/investor_presentation.txt` (output)

**Step 1: Write the extraction script**

Create `scripts/prep_layer_02.py`. This script should:
1. Read the full S-4/A text file.
2. Extract the "RISK FACTORS" section (using regex markers like "RISK FACTORS" header until "CAUTIONARY NOTE" or next major section).
3. Save to `experiments/wework-bowx/data/layer-02/s4_risk_factors.txt`.
4. *Note:* Since we don't have the Investor Presentation text handy in the file list, we'll placeholder copying/creating it. Ideally, we'd extract text from the PDF, but for this plan, we'll assume a text file exists or we create a placeholder.

```python
import re
from pathlib import Path

def main():
    # Setup paths
    base_dir = Path("experiments/wework-bowx")
    s4_path = base_dir / "data/merger/s-4-a/2021-09-17_d166510ds4a.txt"
    output_dir = base_dir / "data/layer-02"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Process S-4 Risk Factors
    print(f"Reading {s4_path}...")
    with open(s4_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Simple extraction logic (adjust based on actual file structure inspection if needed)
    # Looking for "RISK FACTORS" header and stopping before next major section
    # This is a heuristic; might need tuning.
    start_marker = "RISK FACTORS"
    end_marker = "CAUTIONARY NOTE REGARDING FORWARD-LOOKING STATEMENTS"
    
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Warning: Could not find Risk Factors markers. Saving first 100k chars as fallback.")
        risk_text = text[:100000]
    else:
        risk_text = text[start_idx:end_idx]
        print(f"Extracted Risk Factors: {len(risk_text)} chars")

    with open(output_dir / "s4_risk_factors.txt", "w", encoding="utf-8") as f:
        f.write(risk_text)

    # 2. Placeholder for Investor Presentation
    # (Assuming we might manually place it or it exists elsewhere)
    # For now, create a dummy if not exists to unblock config
    inv_deck_path = output_dir / "investor_presentation.txt"
    if not inv_deck_path.exists():
        with open(inv_deck_path, "w") as f:
            f.write("WEWORK INVESTOR PRESENTATION (Placeholder)\n\n[Full text would go here]")

if __name__ == "__main__":
    main()
```

**Step 2: Run preparation**

Run: `.venv/bin/python scripts/prep_layer_02.py`
Expected: Created `s4_risk_factors.txt` and `investor_presentation.txt`.

**Step 3: Commit**

```bash
git add scripts/prep_layer_02.py
git commit -m "feat(layer-02): add data prep script"
```

---

### Task 2: Create Prompts

**Files:**
- Create: `experiments/wework-bowx/layers/02-direct/prompts/naive.md`
- Create: `experiments/wework-bowx/layers/02-direct/prompts/optimized.md`
- Create: `experiments/wework-bowx/layers/02-direct/prompts/system.md`

**Step 1: Create System Prompt**

Write `experiments/wework-bowx/layers/02-direct/prompts/system.md`:
```markdown
You are a financial analyst AI helper.
```

**Step 2: Create Naive Prompt**

Write `experiments/wework-bowx/layers/02-direct/prompts/naive.md`:
```markdown
Based on the following document, answer the question.

Document:
{{document}}

Question: {{question}}
```

**Step 3: Create Optimized Prompt**

Write `experiments/wework-bowx/layers/02-direct/prompts/optimized.md`:
```markdown
You are a senior financial analyst conducting due diligence on a SPAC merger.
Your task is to analyze the provided document and answer the following question.

Rules:
1. Base your answer ONLY on the provided document.
2. Cite specific page numbers or section headers for every claim.
3. If the document does not contain the information, say "Not found in document".
4. Rate your confidence: HIGH (directly stated), MEDIUM (derived/calculated), LOW (inferred).
5. Note any caveats or limitations in the data.

Document:
{{document}}

Question: {{question}}

Provide your answer with citations:
```

**Step 4: Commit**

```bash
git add experiments/wework-bowx/layers/02-direct/prompts/
git commit -m "feat(layer-02): add prompt templates"
```

---

### Task 3: Create Layer Config

**Files:**
- Create: `experiments/wework-bowx/layers/02-direct/config.yaml`

**Step 1: Define Config**

We'll define TWO experiments in one file? Or simpler: Two config files, `config_naive.yaml` and `config_optimized.yaml` to run them separately and cleanly. Let's do `config.yaml` for Optimized (the main one) and `config_naive.yaml` for baseline comparison.

Write `experiments/wework-bowx/layers/02-direct/config.yaml` (Optimized):
```yaml
layer:
  id: "02-direct-optimized"
  name: "Direct LLM (Optimized)"
  description: |
    Direct analysis of specific documents (Investor Deck, S-4 Risk Factors)
    using optimized analyst prompts.

  documents:
    - experiments/wework-bowx/data/layer-02/investor_presentation.txt
    - experiments/wework-bowx/data/layer-02/s4_risk_factors.txt

  prompts:
    system: prompts/system.md
    user: prompts/optimized.md

  models:
    - claude-sonnet-4-5
    - gpt-5.2
    - claude-opus-4-5
    # Exclude Gemini for now due to 500 errors

  evaluation:
    criteria:
      - accurate
      - cited
      - relevant
    outputs:
      - responses

ground_truth: ../../ground-truth/questions.yaml
output_dir: ../../../../results/wework-bowx/layers/02-direct/optimized
```

Write `experiments/wework-bowx/layers/02-direct/config_naive.yaml` (Naive):
```yaml
layer:
  id: "02-direct-naive"
  name: "Direct LLM (Naive)"
  description: |
    Direct analysis of specific documents using naive prompts.
    Baseline for prompt engineering impact.

  documents:
    - experiments/wework-bowx/data/layer-02/investor_presentation.txt
    - experiments/wework-bowx/data/layer-02/s4_risk_factors.txt

  prompts:
    system: prompts/system.md
    user: prompts/naive.md

  models:
    - claude-sonnet-4-5
    - gpt-5.2

ground_truth: ../../ground-truth/questions.yaml
output_dir: ../../../../results/wework-bowx/layers/02-direct/naive
```

**Step 2: Commit**

```bash
git add experiments/wework-bowx/layers/02-direct/config*.yaml
git commit -m "feat(layer-02): add layer configs"
```

---

### Task 4: Verify Run (Dry Run)

**Files:**
- Verify: `scripts/run.py` logic supports `documents` list.

**Step 1: Check Runner Logic (Mental Check)**
- Does `run.py` inject `{{document}}` into the prompt?
- Looking at `dealsignals/experiment/runner.py` (read previously), `_build_user_prompt` replaces `{{question}}`.
- **GAP:** It does NOT currently seem to handle `{{document}}` or iterating over documents.
- **Requirement:** We need to update `ExperimentRunner` to handle document iteration.

**Step 2: Update Runner for Documents**

Modify `dealsignals/experiment/runner.py`:
- Update `run()` to loop over documents if provided in definition.
- Update `_build_user_prompt` to inject `{{document}}` content.
- Update `RunEvent` and `state` to track `document` as well (or just include it in the `question_id` key like `doc1_q1`? No, better to add `document` field to state key).

**Revised Runner Logic:**
1. If `layer.documents` is present:
   - For each `model`:
     - For each `document`:
       - For each `question`:
         - Generate task.
2. State key becomes `(model, document, question_id)`.

**Step 3: Update `ExperimentDefinition`**
- Ensure `documents` field is parsed from YAML.

**Step 4: Run Dry Run**

Run: `.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config_naive.yaml --dry-run`
Expected: List of tasks including document names.

**Step 5: Commit Runner Changes**

```bash
git add dealsignals/experiment/runner.py dealsignals/experiment/definition.py dealsignals/experiment/state.py
git commit -m "feat: support document iteration in experiment runner"
```

---

### Task 5: Final Execution

**Step 1: Run Naive Experiment**

Run: `.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config_naive.yaml`

**Step 2: Run Optimized Experiment**

Run: `.venv/bin/python scripts/run.py --config experiments/wework-bowx/layers/02-direct/config.yaml`

**Step 3: Verify Results**

Check `results/wework-bowx/layers/02-direct/` for output files.
