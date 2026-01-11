from pydantic import BaseModel, Field
from typing import Optional


class TenantCreate(BaseModel):
    name: str = Field(..., example="ACME_CORP")
    size: Optional[int] = Field(None, example=100)


class TenantResponse(BaseModel):
    tenant_id: int = Field(..., example=2)
    name: str = Field(..., example="ACME_CORP")
    size: Optional[int] = Field(None, example=100)
	
class AssignUserToTenantResponse(BaseModel):
    message: str = Field(..., example="User assigned to tenant")