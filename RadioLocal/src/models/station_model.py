from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Station(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: str
    logo_url: str
    stream_url: str
    user_id: Optional[str] = None  # will always be taken from JWT

    @validator("id", pre=True)
    def objectid_to_str(cls, v):
        return str(v)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "_id": "693428a6a77b514aed6e8af4",
                "name": "Radio Banovina",
                "description": "Slušaju svi - slušajte i vi!",
                "logo_url": "https://www.radio-banovina.hr/wp-content/uploads/2015/01/logo-120_00000.png",
                "stream_url": "https://audio.radio-banovina.hr:9998/stream",
                "user_id": "59e482b3-254e-4f7f-be90-da716e8c5035"
            }
        }