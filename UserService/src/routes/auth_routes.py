from fastapi import APIRouter, Depends, HTTPException, status
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.multitenancy.asyncio import list_all_tenants

from src.database import get_current_user, create_tenant, assign_user_to_tenant, get_company_by_user_id
from src.models.tenant_model import TenantResponse, TenantCreate, AssignUserToTenantResponse
from src.models.company_model import CompanyResponse

router = APIRouter(tags=["authentication"])



# Add routes for both with and without trailing slash
async def get_session_info(s: SessionContainer = Depends(verify_session())):
    """Return JWT Seasson to be used in RadioLocal service"""
    jwt = get_current_user(
        s.get_user_id(),
        s.get_access_token_payload()["exp"]
    )
    return {"jwt": jwt}
router.get("/sessioninfo")(get_session_info)
#router.get("/sessioninfo/")(get_session_info)

@router.post(
    "/tenant",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tenant",
    description="Creates a new tenant and returns its identifier.",
)
async def create_new_tenant(
    tenant: TenantCreate,
    s: SessionContainer = Depends(verify_session())
):
    tenant_id = create_tenant(tenant.name, tenant.size)
    return {
        "tenant_id": tenant_id,
        "name": tenant.name,
        "size": tenant.size,
    }

@router.post(
    "/tenant/{tenant_id}/users/{user_id}",
    response_model=AssignUserToTenantResponse,
    status_code=status.HTTP_200_OK,
    summary="Assign user to tenant",
    description="Assigns an existing user to an existing tenant.",
)
async def add_user_to_tenant(
    tenant_id: int,
    user_id: str,
    s: SessionContainer = Depends(verify_session()),
):
    assign_user_to_tenant(user_id, tenant_id)
    return {"message": "User assigned to tenant"}

@router.get(
    "/me/company",
    response_model=CompanyResponse,
    summary="Get company of current user",
    description="Returns the company (tenant) the authenticated user belongs to.",
)
async def get_my_company(
    s: SessionContainer = Depends(verify_session()),
):
    return get_company_by_user_id(s.get_user_id())