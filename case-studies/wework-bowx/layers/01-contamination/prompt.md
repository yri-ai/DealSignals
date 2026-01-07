# Contamination Baseline Prompt

## System Prompt

```
You are a financial analyst assistant. Answer questions based only on your training knowledge. Do not speculate or make up information. If you don't know something, say so clearly.

For each question, provide:
1. Your answer based on what you know from training
2. Confidence level: HIGH (certain), MEDIUM (likely but uncertain), LOW (guessing/uncertain)
3. Note if this is general knowledge or specific to the WeWork/BowX case
```

## User Prompt

```
I'm testing your pre-existing knowledge about the WeWork SPAC merger with BowX Acquisition Corp in 2021. Please answer the following questions based ONLY on what you know from your training data. Do NOT make up information.

## General Knowledge Questions

1. What do you know about the WeWork SPAC merger with BowX in 2021? Describe the basic facts: parties involved, timeline, valuation.

2. What happened to WeWork after the SPAC merger? Describe the company's trajectory from 2021 onwards.

3. What were the main risks or concerns about WeWork at the time of the SPAC merger?

## Specific Financial Questions

4. What was WeWork's implied enterprise value in the BowX merger?

5. What were WeWork's revenue projections for 2021-2025 in the merger documents?

6. What were WeWork's total lease obligations at the time of the merger?

7. What was the cash runway or cash position disclosed in the merger?

## Deal Structure Questions

8. Who were the main parties in the SPAC transaction (sponsor, PIPE investors)?

9. What was SoftBank's stake before and after the merger?

10. What protections or rights did PIPE investors receive?

## Risk Factor Questions

11. What were the top risk factors disclosed in the S-4 registration statement?

12. Were there any going concern warnings in the filings?

13. What litigation or regulatory issues were disclosed?

## Outcome Questions

14. Did WeWork achieve its projected profitability timeline?

15. What ultimately happened to WeWork? (bankruptcy, restructuring, etc.)

---

For each answer, indicate:
- [HIGH/MEDIUM/LOW] confidence
- [TRAINING] if from pre-training knowledge or [UNCERTAIN] if you're not sure

If you don't know the answer to any question, say "I don't have reliable information about this" rather than guessing.
```

## Expected Output Format

The model should provide numbered responses with confidence indicators. This helps map which questions have high contamination risk (model knows answer from training) vs. low contamination risk (model needs documents to answer).

## Analysis Guide

After running this prompt:

1. **High Contamination** (HIGH confidence, correct answer): Model knows this from training. Results on related eval questions may reflect training, not document analysis.

2. **Medium Contamination** (MEDIUM confidence, partially correct): Model has some training knowledge. Results need careful interpretation.

3. **Low Contamination** (LOW confidence or "don't know"): Model needs documents. These are the cleanest test questions.

4. **Hallucination Risk** (HIGH confidence, wrong answer): Model confabulates. Red flag for reliability.
