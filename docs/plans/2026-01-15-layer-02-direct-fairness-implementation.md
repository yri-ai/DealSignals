# Layer 02 Direct Fairness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Layer 02 “Direct LLM” fair and usable by generating deterministic, truncated full-document inputs without retrieval.

**Architecture:** Add a deterministic section-parsing + truncation step in `scripts/prep_layer_02.py` that produces bounded inputs and a metadata sidecar. Keep configs unchanged; update README to document the protocol.

**Tech Stack:** Python 3.13+, uv, existing project scripts.

---

### Task 1: Add deterministic section parsing + truncation helpers

**Files:**
- Modify: `scripts/prep_layer_02.py`
- Create: `tests/test_prep_layer_02.py`

**Step 1: Write the failing test**
```python
# tests/test_prep_layer_02.py

def test_section_priority_truncation_prefers_ordered_sections():
    text = """
RISK FACTORS\nRisk content...\nSUMMARY\nSummary content...\nFINANCIAL DATA\nFinancial content...\n"""
    sections = parse_sections(text, ["RISK FACTORS", "SUMMARY", "FINANCIAL DATA"])
    truncated = truncate_sections(sections, ["SUMMARY", "RISK FACTORS"], budget_chars=40)
    assert truncated.startswith("SUMMARY")
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_prep_layer_02.py::test_section_priority_truncation_prefers_ordered_sections -v`
Expected: FAIL (helpers not implemented)

**Step 3: Write minimal implementation**
```python
# scripts/prep_layer_02.py

def parse_sections(text: str, headers: list[str]) -> dict[str, str]:
    ...

def truncate_sections(sections: dict[str, str], priority: list[str], budget_chars: int) -> str:
    ...
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_prep_layer_02.py::test_section_priority_truncation_prefers_ordered_sections -v`
Expected: PASS

**Step 5: Commit**
```bash
git add scripts/prep_layer_02.py tests/test_prep_layer_02.py
git commit -m "feat: add deterministic truncation helpers"
```

---

### Task 2: Implement Layer 02 prep pipeline + metadata output

**Files:**
- Modify: `scripts/prep_layer_02.py`
- Create: `experiments/wework-bowx/data/layer-02/layer-02_meta.json`

**Step 1: Write the failing test**
```python
# tests/test_prep_layer_02.py

def test_prep_writes_metadata(tmp_path, monkeypatch):
    # stub paths, call main(), assert metadata file exists
    assert (tmp_path / "layer-02_meta.json").exists()
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_prep_layer_02.py::test_prep_writes_metadata -v`
Expected: FAIL (no metadata yet)

**Step 3: Write minimal implementation**
```python
# scripts/prep_layer_02.py
# - remove placeholder investor presentation write
# - require real investor presentation source
# - generate truncated outputs for S-4 + investor deck
# - emit layer-02_meta.json with hashes, budgets, and section coverage
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_prep_layer_02.py::test_prep_writes_metadata -v`
Expected: PASS

**Step 5: Commit**
```bash
git add scripts/prep_layer_02.py tests/test_prep_layer_02.py
git commit -m "feat(layer-02): generate deterministic inputs and metadata"
```

---

### Task 3: Document the truncation protocol

**Files:**
- Modify: `experiments/wework-bowx/layers/02-direct/README.md`

**Step 1: Write the failing test**
```python
# tests/test_prep_layer_02.py

def test_readme_mentions_truncation_protocol():
    content = Path("experiments/wework-bowx/layers/02-direct/README.md").read_text()
    assert "truncation" in content.lower()
```

**Step 2: Run test to verify it fails**
Run: `pytest tests/test_prep_layer_02.py::test_readme_mentions_truncation_protocol -v`
Expected: FAIL

**Step 3: Write minimal implementation**
```md
# README
- Document the deterministic truncation protocol
- Note that the investor presentation must be real (no placeholders)
- Explain metadata sidecar usage
```

**Step 4: Run test to verify it passes**
Run: `pytest tests/test_prep_layer_02.py::test_readme_mentions_truncation_protocol -v`
Expected: PASS

**Step 5: Commit**
```bash
git add experiments/wework-bowx/layers/02-direct/README.md tests/test_prep_layer_02.py
git commit -m "docs(layer-02): document fairness truncation protocol"
```

---

### Task 4: Run prep + verify outputs

**Files:**
- Modify: none

**Step 1: Run prep**
Run: `.venv/bin/python scripts/prep_layer_02.py`
Expected: Writes `s4_risk_factors.txt`, `investor_presentation.txt`, `layer-02_meta.json`

**Step 2: Verify sizes and metadata**
Run: `ls -lh experiments/wework-bowx/data/layer-02/`
Expected: Non-empty files and metadata present

**Step 3: Commit (if any generated artifacts are meant to be tracked)**
```bash
git status -sb
```
Expected: Only intended tracked files are modified

---

## Notes / Decisions Needed Before Implementation
- Confirm the *real* investor presentation source file path (currently missing).
- Confirm budgets (chars or tokens) and whether to enable rotation mode.

## Verification
- Run `pytest` after each task step.
- Use `ruff check .` if linting changes are introduced.
