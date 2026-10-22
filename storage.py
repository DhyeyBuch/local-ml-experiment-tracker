import json
from pathlib import Path
import os
import tempfile

def save_experiment(experiments, filename):
    destination = Path(filename)
    text = json.dumps(experiments, indent=2, allow_nan=False)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent, delete=False) as file:
            temporary_path = Path(file.name)
            file.write(text)

        os.replace(temporary_path, destination)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    

def load_experiment(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            loaded_experiments = json.load(file)

            if not isinstance(loaded_experiments, list):
                raise TypeError("Experiment file must contain a list")
            
    except FileNotFoundError:
        return []
    return loaded_experiments