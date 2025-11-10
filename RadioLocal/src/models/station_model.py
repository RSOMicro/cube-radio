from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Station(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: str
    logo_url: str
    stream_url: str
    company_id: Optional[str] = None  # will always be taken from JWT

    @validator("id", pre=True)
    def objectid_to_str(cls, v):
        return str(v)

    class Config:
        arbitrary_types_allowed = True