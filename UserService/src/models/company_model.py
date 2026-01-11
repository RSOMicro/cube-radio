from pydantic import BaseModel, Field
from typing import Optional


class CompanyResponse(BaseModel):
    tenant_id: int = Field(..., example=1)
    tenant_name: str = Field(..., example="DEFAULT_PUBLIC")
    tenant_size: Optional[int] = Field(None, example=999)