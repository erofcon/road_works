from fastapi import APIRouter, HTTPException, Depends, status

from loguru import logger

from app.crud import company as companies_crud
from app.schemas import company as companies_schemas
from app.schemas import user as user_schemas
from app.crud import user as user_crud

router = APIRouter()


@router.post('/create_company')
async def create_company(company: companies_schemas.CompanyCreate,
                         current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    """
    Only admin can create company!
    """

    if not current_user.is_admin:
        logger.error(f"error create company by {current_user.username}. User not admin")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if await companies_crud.get_company_by_name(company.name):
        logger.error(f"error create company by {current_user.username}. Company exists")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Company exists')

    if not await companies_crud.create_company(company=company):
        logger.error(f"error create company by {current_user.username}. An error has occurred")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    logger.success(f"create company by {current_user.username}")
    return HTTPException(status_code=status.HTTP_201_CREATED)
