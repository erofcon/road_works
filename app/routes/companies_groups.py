from fastapi import APIRouter, HTTPException, status

from app.crud import companies_groups as companies_groups_crud
from app.schemas import companies_groups as companies_groups_schemas

router = APIRouter()


@router.post('/create_related_companies_groups')
async def create_related_companies_groups(companies_groups: companies_groups_schemas.CompaniesGroupsBaseCreate):
    if not await companies_groups_crud.create_related_companies_groups(companies_groups=companies_groups):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)
