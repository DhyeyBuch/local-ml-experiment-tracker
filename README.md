# ML Experiment Tracker

A Python application for recording ML experiments through a command-line
interface or REST API. Both interfaces use the same SQLite database.

## Features

- Record model, dataset, parameters, metric, and notes
- Retrieve experiments by ID
- List experiments through the CLI
- Filter and paginate experiments through the API
- Update experiment notes
- Validate inputs before insertion

## Setup

Requires Python 3.12. Developed using WSL/Linux.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The database is created automatically on first use.

## Run the API

```bash
python -m uvicorn api:app --reload --port 8001
```

Open http://127.0.0.1:8001/docs for interactive API documentation.

Available endpoints:

- GET /health
- GET /experiments
- GET /experiments/{experiment_id}
- POST /experiments
- PATCH /experiments/{experiment_id}

The list endpoint accepts dataset_name, model_name, offset, and limit.

## Use the CLI

```bash
python main.py add \
  --model Ridge \
  --dataset taxi_v1 \
  --metric rmse \
  --value 4.2 \
  --parameters '{"alpha": 1.0}' \
  --notes "Initial baseline"

python main.py list
python main.py show 1
python main.py update-notes 1 "Updated baseline"
```

Replace example IDs with IDs from your database.
The CLI list command currently returns the first 10 records.

## Project structure

- api.py: HTTP endpoints and request models
- main.py: command-line interface
- database.py: SQLite initialization and queries
- tracker.py: experiment validation and earlier in-memory operations
- storage.py: earlier JSON persistence implementation

## Data storage

Current CLI and API operations use experiments.db beside database.py.

## Current limitations

- Intended for local use; authentication is not implemented
- Duplicate experiments are permitted
- Deletion is not supported