# experiment={"id": 1,"model_name": "Ridge","dataset_name": "taxi_v1","parameters": {"alpha": 1.0},"metric_name": "rmse","metric_value": 5.2,"notes": "Initial baseline"}
import math
import json
from storage import save_experiment, load_experiment
from tracker import add_experiment, update_notes, get_experiment

def display_experiments(experiments):
    if experiments:
        for experiment in experiments:
            print(experiment)
    else:
        print("No experiments recorded")

def main():
    FILENAME = "taxi_exp.json"

    experiments = load_experiment(FILENAME)

    try:
        add_experiment(
            experiments,
            model_name="   ",
            dataset_name="taxi_v2",
            parameters={},
            metric_name="RMSE",
            metric_value=3.8
        )
    except (ValueError, TypeError) as error:
        print(f"Rejected: {error}")

    else:
        save_experiment(experiments, FILENAME)
        print("Successfully Added and Saved")

    try:
        new_rec = update_notes(experiments, 2, "Best performing so far")
    except TypeError as error:
        print(f"Rejected: {error}")
    else:
        if new_rec is None:
            print("Experiment not found")
        else:
            save_experiment(experiments, FILENAME)
            display_experiments(load_experiment(FILENAME))

    record = get_experiment(experiments, experiment_id=92)

    if record is None:
        print("Experiment is not found")
    else:
        print(record["model_name"])

if __name__=="__main__":
    main()
