#!/usr/bin/env python3
"""
Run contamination baseline test for WeWork/BowX case study.

Tests what LLMs know from training data before seeing any documents.

Usage:
    python run_contamination.py --model claude
    python run_contamination.py --model gpt4
    python run_contamination.py --all
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from lib.llm import call_llm, save_response, LLMConfig

# Model configurations
MODELS = {
    "claude": LLMConfig(
        provider="anthropic",
        model="claude-sonnet-4-20250514",
        temperature=0.0,
        max_tokens=8192,
    ),
    "gpt4": LLMConfig(
        provider="openai",
        model="gpt-4o",
        temperature=0.0,
        max_tokens=8192,
    ),
}

SYSTEM_PROMPT = """You are a financial analyst assistant. Answer questions based only on your training knowledge. Do not speculate or make up information. If you don't know something, say so clearly.

For each question, provide:
1. Your answer based on what you know from training
2. Confidence level: HIGH (certain), MEDIUM (likely but uncertain), LOW (guessing/uncertain)
3. Note if this is general knowledge or specific to the WeWork/BowX case"""

USER_PROMPT = """I'm testing your pre-existing knowledge about the WeWork SPAC merger with BowX Acquisition Corp in 2021. Please answer the following questions based ONLY on what you know from your training data. Do NOT make up information.

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

If you don't have reliable information about any question, say "I don't have reliable information about this" rather than guessing."""


def run_contamination_test(model_name: str) -> dict:
    """Run contamination test for a single model."""
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}. Choose from: {list(MODELS.keys())}")

    config = MODELS[model_name]
    print(f"\n{'=' * 60}")
    print(f"Running contamination test: {model_name}")
    print(f"Model: {config.model}")
    print(f"{'=' * 60}\n")

    response = call_llm(USER_PROMPT, config, system=SYSTEM_PROMPT)

    print(f"Completed in {response.latency_ms}ms")
    print(f"Tokens: {response.input_tokens} in, {response.output_tokens} out")

    return response


def main():
    parser = argparse.ArgumentParser(description="Run contamination baseline test")
    parser.add_argument("--model", choices=list(MODELS.keys()), help="Model to test")
    parser.add_argument("--all", action="store_true", help="Test all models")
    parser.add_argument("--anthropic-key", help="Anthropic API key (or set ANTHROPIC_API_KEY)")
    parser.add_argument("--openai-key", help="OpenAI API key (or set OPENAI_API_KEY)")
    args = parser.parse_args()

    if not args.model and not args.all:
        parser.print_help()
        sys.exit(1)

    # Set API keys from args if provided
    if args.anthropic_key:
        MODELS["claude"].api_key = args.anthropic_key
    if args.openai_key:
        MODELS["gpt4"].api_key = args.openai_key

    # Create runs directory
    runs_dir = Path(__file__).parent / "runs"
    runs_dir.mkdir(exist_ok=True)

    models_to_run = list(MODELS.keys()) if args.all else [args.model]

    results = {}
    for model_name in models_to_run:
        try:
            response = run_contamination_test(model_name)

            # Save response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = runs_dir / f"{model_name}_{timestamp}.json"
            save_response(response, str(output_path))
            print(f"Saved: {output_path}")

            # Also save readable markdown
            md_path = runs_dir / f"{model_name}_{timestamp}.md"
            with open(md_path, "w") as f:
                f.write(f"# Contamination Baseline: {model_name}\n\n")
                f.write(f"**Model:** {response.model}\n")
                f.write(f"**Timestamp:** {response.timestamp}\n")
                f.write(f"**Latency:** {response.latency_ms}ms\n")
                f.write(f"**Tokens:** {response.input_tokens} in, {response.output_tokens} out\n\n")
                f.write("---\n\n")
                f.write(response.content)
            print(f"Saved: {md_path}")

            results[model_name] = "success"

        except Exception as e:
            print(f"Error running {model_name}: {e}")
            results[model_name] = f"error: {e}"

    print("\n" + "=" * 60)
    print("Summary:")
    for model, status in results.items():
        print(f"  {model}: {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
