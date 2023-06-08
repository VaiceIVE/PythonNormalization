from pydantic import BaseModel

class NormalizationDataIncidents(BaseModel):
    incidents: list

class NormalizationDataWorks(BaseModel):
    works: list
    