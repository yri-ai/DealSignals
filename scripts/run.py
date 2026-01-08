#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dealsignals.experiment import ExperimentDefinition, ExperimentRunner


def main():
    parser = argparse.ArgumentParser(description="Run DealSignals experiments")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to layer config.yaml",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help="Specific models to run (space-separated)",
    )
    parser.add_argument(
        "--questions",
        nargs="+",
        help="Specific question IDs to run (space-separated)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would run without executing",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current run status",
    )
    args = parser.parse_args()

    definition = ExperimentDefinition.from_yaml(args.config)
    runner = ExperimentRunner(definition)

    if args.status:
        status = runner.status()
        print(f"Layer: {definition.layer.id}")
        print(f"Completed: {status['completed']}")
        print(f"Failed: {status['failed']}")
        print(f"Models: {', '.join(status['models']) if status['models'] else 'none'}")
        print(f"Questions: {len(status['questions'])}")
        return

    def on_progress(model: str, question_id: str, status: str):
        print(f"  [{model}] {question_id}: {status}")

    print(f"Running experiment: {definition.layer.name}")
    print(f"Output: {definition.output_dir}")
    print()

    summary = runner.run(
        models=args.models,
        questions=args.questions,
        dry_run=args.dry_run,
        on_progress=on_progress,
    )

    print()
    print("=" * 60)
    print(f"Run ID: {summary.run_id}")
    print(f"Completed: {summary.completed}")
    print(f"Failed: {summary.failed}")
    print(f"Total Cost: ${summary.total_cost_usd:.4f}")
    print(f"Total Tokens: {summary.total_tokens:,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
