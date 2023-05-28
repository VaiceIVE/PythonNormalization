from pydantic import BaseModel

class NormalizationData(BaseModel):
    incidents: list
    works: list
    