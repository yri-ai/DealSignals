import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="ds",
        description="DealSignals - AI Research for Deal Analysis",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    run_parser = subparsers.add_parser("run", help="Run an experiment")
    run_parser.add_argument("--config", type=Path, required=True, help="Path to config.yaml")
    run_parser.add_argument("--models", nargs="+", help="Models to run")
    run_parser.add_argument("--questions", nargs="+", help="Question IDs to run")
    run_parser.add_argument("--dry-run", action="store_true", help="Show what would run")

    status_parser = subparsers.add_parser("status", help="Show experiment status")
    status_parser.add_argument("--config", type=Path, required=True, help="Path to config.yaml")

    models_parser = subparsers.add_parser("models", help="List available models")

    args = parser.parse_args()

    if args.command == "run":
        _run_experiment(args)
    elif args.command == "status":
        _show_status(args)
    elif args.command == "models":
        _list_models()
    else:
        parser.print_help()


def _run_experiment(args):
    from dealsignals.experiment import ExperimentDefinition, ExperimentRunner

    definition = ExperimentDefinition.from_yaml(args.config)
    runner = ExperimentRunner(definition)

    def on_progress(model: str, question_id: str, status: str):
        print(f"  [{model}] {question_id}: {status}")

    print(f"Running: {definition.layer.name}")
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
    print(f"Cost: ${summary.total_cost_usd:.4f}")
    print(f"Tokens: {summary.total_tokens:,}")
    print("=" * 60)


def _show_status(args):
    from dealsignals.experiment import ExperimentDefinition, ExperimentRunner

    definition = ExperimentDefinition.from_yaml(args.config)
    runner = ExperimentRunner(definition)
    status = runner.status()

    print(f"Layer: {definition.layer.id}")
    print(f"Completed: {status['completed']}")
    print(f"Failed: {status['failed']}")
    print(f"Models: {', '.join(status['models']) if status['models'] else 'none'}")
    print(f"Questions: {len(status['questions'])}")


def _list_models():
    from dealsignals.providers import get_registry

    registry = get_registry()

    print("Aliases:")
    for alias, model_id in sorted(registry.list_aliases().items()):
        print(f"  {alias:12} -> {model_id}")

    print()
    print("Available models:")
    try:
        for model in registry.list_all_models():
            price = f"${model.input_price_per_m:.2f}/{model.output_price_per_m:.2f}"
            print(f"  {model.id:40} {price:>15}")
    except Exception as e:
        print(f"  (Could not fetch models: {e})")


if __name__ == "__main__":
    main()
