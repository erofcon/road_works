from fastapi import APIRouter, HTTPException, status

from app.crud import companies as companies_crud
from app.schemas import companies as companies_schemas

router = APIRouter()


@router.post('/create_company')
async def create_company(company: companies_schemas.CompaniesCreate):
    if await companies_crud.get_company_by_name(company.name):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Company exists')

    if not await companies_crud.create_company(company=company):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)
