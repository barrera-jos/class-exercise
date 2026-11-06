from pydantic import BaseModel, Field

class MovieInput(BaseModel):
    title: str
    release_year: int


class MovieResponse(MovieInput):
    id: int
    
class CSVInfo(BaseModel):
    filename: str
    columns: int
    column_names: list[str]
    data_set: int
    


class ProcessingSettings(BaseModel):
    remove_duplicates: bool = True
    drop_missing: bool = True
    

class ProcessConfig(BaseModel):
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)