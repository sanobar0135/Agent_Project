from pydantic import BaseModel,Field
class ResearchRequest(BaseModel):
    topic:str=Field(min_length=5,max_length=500)
