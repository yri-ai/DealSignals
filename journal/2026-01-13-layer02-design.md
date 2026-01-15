# Layer 02 Design Decisions

**Date:** 2026-01-13
**Context:** Preparing Layer 02 (Direct LLM Naive) baseline experiment

## Document Size Analysis

### S-4/A Filing (2021-09-17)
The primary document for human ground truth analysis.

| Metric | markitdown | BeautifulSoup (text only) |
|--------|------------|---------------------------|
| HTML file size | 10.9 MB | 10.9 MB |
| Output characters | 11.4M | 4.2M |
| Word count | 1,136,974 | 667,974 |
| **Estimated tokens** | **~2.85M** | **~1.05M** |

**Decision:** Use BeautifulSoup text extraction (cleaner, smaller) over markitdown (retains HTML artifacts).

Even with clean text extraction, the document is ~1 million tokens - still exceeds all context windows.

### Context Window Comparison

| Model | Context Window | S-4 Tokens | Fit? | Ratio |
|-------|----------------|------------|------|-------|
| Claude Opus 4.5 | 200K | 2.85M | No | 14.3x over |
| Claude Sonnet 4.5 | 200K | 2.85M | No | 14.3x over |
| GPT-5.2 | 128K | 2.85M | No | 22.3x over |
| Gemini 3 Pro | 1M | 2.85M | No | 2.85x over |
| Gemini 3 Flash | 1M | 2.85M | No | 2.85x over |

**Key Finding:** No current model can fit the full S-4/A in context. Even Gemini's 1M context is insufficient.

## Decision: Document Handling Strategy

### Options Considered

1. **Full Document Truncation**
   - Pros: Simple, reproducible
   - Cons: Loses critical information in later sections (risk factors, financials often at end)
   - Decision: Not viable for research quality

2. **Key Sections Extraction**
   - Pros: Fits context, preserves most important content
   - Cons: Requires manual section identification, may miss unexpected signals
   - Decision: Use for Layer 02 baseline

3. **RAG (Retrieval Augmented Generation)**
   - Pros: Can search full document, retrieves relevant chunks per question
   - Cons: More complex, retrieval quality affects results
   - Decision: Reserved for Layer 03+

4. **Hierarchical Summarization**
   - Pros: Can compress full document
   - Cons: Lossy, may miss details, adds another model step
   - Decision: Reserved for Layer 05+

### Selected Approach: Key Sections Extraction

For Layer 02 (Direct LLM Naive), we will extract key sections from the S-4/A that contain the information needed for ground truth questions:

**Priority Sections:**
1. Summary / Prospectus Summary
2. Risk Factors (pages 34-80+)
3. Selected Financial Data
4. Management's Discussion and Analysis (MD&A)
5. Business Description
6. Certain Projected Financial Information
7. Unaudited Pro Forma Financial Information

**Target:** Extract sections totaling ~150K tokens to fit in 200K context with room for prompt/response.

## Tools Decision

### HTML to Markdown Conversion
**Selected:** [markitdown](https://github.com/microsoft/markitdown) by Microsoft

**Rationale:**
- Handles complex HTML tables (critical for SEC filings)
- Preserves document structure
- Active maintenance
- Simple API

**Alternative Considered:** Custom BeautifulSoup extraction
- Rejected: More work, less robust table handling

## Implementation Plan

1. Convert full S-4/A to markdown (done)
2. Identify section boundaries in markdown
3. Extract key sections to separate file
4. Create Layer 02 config with extracted sections
5. Run baseline with section-based context

## Research Implications

### What This Means for Results

1. **Layer 02 results are section-limited** — Models only see extracted sections, not full filing
2. **Comparison to human baseline** — Human expert read full document; AI sees subset
3. **Question coverage** — Some questions may not be answerable from extracted sections
4. **Future layers** — RAG approach (Layer 03+) will search full document

### Tracking Requirements

For each Layer 02 run, we must record:
- Which sections were included
- Total token count of context
- Any questions that required information outside extracted sections

## Token Counting

For accurate token counting, we should use tiktoken or model-specific tokenizers rather than character estimation.

**TODO:** Add proper token counting to the experiment runner.

## Related Decisions

- **Gemini exclusion (Layer 01):** ZenMux 500 errors, documented in `results/wework-bowx/layers/01-contamination/NOTES.md`
- **Model selection:** Using actual model names (e.g., `claude-opus-4-5`) not aliases
