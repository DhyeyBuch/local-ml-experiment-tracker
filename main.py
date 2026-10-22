import json
import argparse

from tracker import validate_experiment
from database import (
    initialize_database,
    fetch_experiment,
    fetch_experiments,
    insert_experiment,
    update_experiment_notes,
)


def display_experiments(experiments):
    if experiments:
        for experiment in experiments:
            print(experiment)
    else:
        print("No experiments recorded")


def main():
    parser = argparse.ArgumentParser(description="Inspect Saved ML Experiments")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="Display the first 10 experiments")

    show_parser = subparsers.add_parser("show", help="Display one experiment")
    show_parser.add_argument(
        "experiment_id", type=int,
        help="ID of the experiment you want to inspect"
    )

    update_notes_parser = subparsers.add_parser(
        "update-notes", help="Update the notes of the specified experiment"
    )
    update_notes_parser.add_argument(
        "experiment_id", type=int,
        help="ID of the experiment you want to update"
    )
    update_notes_parser.add_argument("notes", help="The updated notes")

    add_parser = subparsers.add_parser("add", help="Add a new experiment")
    add_parser.add_argument("--model", required=True, help="Model name")
    add_parser.add_argument("--dataset", required=True, help="Dataset name")
    add_parser.add_argument("--metric", required=True, help="Metric name")
    add_parser.add_argument(
        "--value", type=float, required=True, help="Metric value"
    )
    add_parser.add_argument("--notes", default="", help="Experiment Notes")
    add_parser.add_argument(
        "--parameters", default="{}",
        help="Model Parameters as a JSON object"
    )

    args = parser.parse_args()

    initialize_database()

    if args.command == "show":
        record = fetch_experiment(args.experiment_id)

        if record is not None:
            print(record)
        else:
            print("Experiment not found")

    elif args.command == "list":
        display_experiments(fetch_experiments())

    elif args.command == "update-notes":
        found = update_experiment_notes(args.experiment_id, args.notes)

        if found:
            print(fetch_experiment(args.experiment_id))
        else:
            print("Experiment doesn't exist")

    elif args.command == "add":
        try:
            parameters = json.loads(args.parameters)
            validate_experiment(
                model_name=args.model,
                dataset_name=args.dataset,
                parameters=parameters,
                metric_name=args.metric,
                metric_value=args.value,
                notes=args.notes,
            )

            json.dumps(parameters, allow_nan=False)

        except (ValueError, TypeError) as error:
            print(f"Rejected: {error}")
        else:
            new_id = insert_experiment(
                model_name=args.model,
                dataset_name=args.dataset,
                parameters=parameters,
                metric_name=args.metric,
                metric_value=args.value,
                notes=args.notes,
            )
            print(f"Saved Experiment: {new_id}")


if __name__ == "__main__":
    main()