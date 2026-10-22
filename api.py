from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from contextlib import asynccontextmanager

from tracker import validate_experiment

from database import fetch_experiment, insert_experiment, fetch_experiments, update_experiment_notes, initialize_database


class ExperimentCreate(BaseModel):
    model_name: str
    dataset_name: str
    parameters: dict
    metric_name: str
    metric_value: float
    notes: str = ""

class NotesUpdate(BaseModel):
    notes: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database
    yield()

app = FastAPI(lifespan=lifespan)
@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/experiments")
def list_experiments(
                    dataset_name: str | None = None, 
                    model_name: str | None = None, 
                    offset: int = Query(default=0, ge=0),
                    limit: int = Query(default=10, ge=1, le=100)
):
    return fetch_experiments(
        dataset_name=dataset_name,
        model_name=model_name,
        offset=offset,
        limit=limit
        )

@app.get("/experiments/{experiment_id}")
def read_experiment(experiment_id: int):
    record = fetch_experiment(experiment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="No such record found")
    return record

@app.post("/experiments", status_code=201)
def create_experiment(data: ExperimentCreate):
    try:
        validate_experiment(data.model_name, data.dataset_name, data.parameters, data.metric_name, data.metric_value, data.notes)
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=422, detail=str(error))
    else:
        new_id = insert_experiment(data.model_name, data.dataset_name, data.parameters, data.metric_name, data.metric_value, data.notes)
        record = fetch_experiment(new_id)
        return record
    

@app.patch("/experiments/{experiment_id}")
def edit_experiment_notes(experiment_id: int, data: NotesUpdate):
    found = update_experiment_notes(experiment_id, data.notes)

    if not found:
        raise HTTPException(status_code=404, detail="No such record found")

    return fetch_experiment(experiment_id)

