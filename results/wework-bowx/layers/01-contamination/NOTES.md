# Layer 01 Contamination Baseline - Research Notes

## Known Issues

### Gemini Models Unavailable (2026-01-13)

**Issue:** `gemini-3-flash` and `gemini-3-pro` return HTTP 500 errors from ZenMux API.

**Error:**
```
Server error '500 Internal Server Error' for url 'https://opencode.ai/zen/v1/chat/completions'
```

**Impact:** Gemini models excluded from Layer 01 contamination baseline testing.

**Models Tested:**
| Model | Status | Notes |
|-------|--------|-------|
| claude-opus-4-5 | OK | Working |
| claude-sonnet-4-5 | OK | Working |
| gpt-5.2 | OK | Working |
| gemini-3-flash | FAILED | 500 error |
| gemini-3-pro | FAILED | 500 error |
| grok-code | OK | Working |
| glm-4.7-free | OK | Working |
| kimi-k2 | OK | Working |

**Resolution:** Excluded Gemini from config. Will re-test when ZenMux resolves upstream issue.

**TODO:** Add Gemini results when available to complete cross-model contamination comparison.

---

## Run History

### 2026-01-13

- Initial test runs with Claude Sonnet 4.5, GPT-5.2
- Claude Opus 4.5 added for comprehensive testing
- Gemini exclusion due to upstream ZenMux issues
- 6 models configured for full run: claude-opus-4-5, claude-sonnet-4-5, gpt-5.2, grok-code, glm-4.7-free, kimi-k2

### Earlier Runs (2026-01-08)

- Failed runs due to missing API key configuration
- These are recorded in events.jsonl but should be ignored for analysis
