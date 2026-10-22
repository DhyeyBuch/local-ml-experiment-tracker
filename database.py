import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "experiments.db"


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY,
                model_name TEXT NOT NULL,
                dataset_name TEXT NOT NULL,
                parameters TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                notes TEXT NOT NULL DEFAULT ''
            )
        """)
        connection.commit()
    finally:
        connection.close()

def insert_experiment(model_name, dataset_name, parameters, metric_name, metric_value, notes=""):
    params = json.dumps(parameters, indent=2, allow_nan=False)
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "INSERT INTO experiments (model_name, dataset_name, parameters, metric_name, metric_value, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (model_name, dataset_name, params, metric_name, metric_value, notes)
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()

def fetch_experiment(experiment_id):
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            "SELECT * FROM experiments WHERE id = ?",
            (experiment_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        record = dict(row)
        record['parameters'] = json.loads(record['parameters'])
        return record
    finally:
        connection.close()

def fetch_experiments(dataset_name=None, model_name=None, offset=0, limit=10):
    conditions = []
    values = []

    if dataset_name is not None:
        conditions.append("dataset_name = ?")
        values.append(dataset_name)

    if model_name is not None:
        conditions.append("model_name = ?")
        values.append(model_name)

    query = "SELECT * FROM experiments"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id LIMIT ? OFFSET ?"
    values.extend([limit, offset])

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(query, values).fetchall()

        experiments = []

        for row in rows:
            record = dict(row)
            record['parameters'] = json.loads(record['parameters'])
            experiments.append(record)

        return experiments

    finally:
        connection.close()

def update_experiment_notes(experiment_id, notes):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "UPDATE experiments SET notes = ? WHERE id = ?",
            (notes, experiment_id)
        )

        connection.commit()

        return cursor.rowcount > 0
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()