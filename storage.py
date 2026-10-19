import json

def save_experiment(experiments, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(experiments, file, indent=2, allow_nan=False)

def load_experiment(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            loaded_experiments = json.load(file)

            if not isinstance(loaded_experiments, list):
                raise TypeError("Experiment file must contain a list")
            
    except FileNotFoundError:
        return []
    return loaded_experiments