#main.py

from fastapi import FastAPI, Query
from fastapi import Query
from src import MovieInput, CSVInfo, MovieResponse, ProcessConfig
from fastapi import File, UploadFile, HTTPException
import logging
from pathlib import Path
import io
import pandas as pd
from src.storage import DataStorage
from middleware import log_requests



app = FastAPI(title="Movie API")
storage = DataStorage()


@app.get("/health")
def health_check():
    return {"status": "ok"}

#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.



demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record

@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}

logger = logging.getLogger(__name__)

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    
    suffix = Path(file.filename or "").suffix.lower()
    if suffix != ".csv":
        logger.warning(f"Rejected upload '{file.filename}': not a CSV file")
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        logger.warning(f"Could not parse '{file.filename}': {e}")
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {e}") from e


    dataset_id = storage.save_data(df, file.filename)
    logger.info(f"Saved dataset {dataset_id} from '{file.filename}'")

    return CSVInfo(
        dataset_id=dataset_id,
        filename=file.filename,
        shape=df.shape,
        columns=df.columns.tolist(),
    )
storage = DataStorage()

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    df = storage.get_data(dataset_id)
    if df is None:
        logger.warning(f"Dataset {dataset_id} not found")
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")

    logger.info(f"Retrieved dataset {dataset_id}")
    rows, columns = df.shape
    return {"dataset_id": dataset_id, "rows": rows, "columns": columns}

@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()

    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()
        
    if settings['processing']['drop_missing']:
        df = df.dropna()
        
    return {"rows": len(df)}

app.middleware("http")(log_requests)