import math

def validate_nonblank_string(field_name, value):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} should be a string")
    if not value.split():
        raise ValueError(f"{field_name} should not be empty")

def validate_metric_value(metric_value):
    if isinstance(metric_value, bool):
        raise TypeError("Metric Value should not be a boolean value")
    if not isinstance(metric_value, (int, float)):
        raise TypeError("Metric Value should be an integer or float value")
    if not math.isfinite(metric_value):
        raise ValueError("Metric Value should be finite")

def validate_experiment(model_name, dataset_name, parameters, metric_name, metric_value, notes=""):
    validate_nonblank_string("Model Name", model_name)
    validate_nonblank_string("Dataset Name", dataset_name)
    validate_nonblank_string("Metric Name", metric_name)
    validate_metric_value(metric_value)

    if not isinstance(parameters, dict):
        raise TypeError("Parameters should be a dictionary")

    if not isinstance(notes, str):
        raise TypeError("Notes should be a string")

def add_experiment(experiments, model_name, dataset_name, parameters, metric_name, metric_value, notes=''):
    validated = validate_experiment(model_name, dataset_name, parameters, metric_name, metric_value, notes)

    if validated:
        experiment_id = experiments[-1]["id"] + 1 if experiments else 1
        experiment = {"id":experiment_id, "model_name":model_name, "dataset_name":dataset_name, "parameters":parameters, "metric_name":metric_name, "metric_value":metric_value, "notes":notes}
        experiments.append(experiment)
        return experiment

def get_experiment(experiments, experiment_id):
    for experiment in experiments:
        if experiment["id"]==experiment_id:
            return experiment
    return None

def update_notes(experiments, experiment_id, notes):
    if not isinstance(notes, str):
        raise TypeError("Notes should be a string")
    record = get_experiment(experiments, experiment_id)

    if record is not None:
        record["notes"] = notes
        return record
    return None