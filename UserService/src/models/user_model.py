from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: str
    name: str
    lastname: str
    company_id: Optional[int] = None

class UserOut(BaseModel):
    user_id: UUID
    email: str
    name: str
    lastname: str
    company_id: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "de51a1d9-e6d5-4109-9828-49dc7bba3449",
                "email": "john.doe@example.com",
                "name": "John",
                "lastname": "Doe",
                "company_id": 1
            }
        }