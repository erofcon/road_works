from pydantic import BaseModel


class CompaniesGroupsBase(BaseModel):
    company_id: int
    group_id: int


class CompaniesGroupsBaseCreate(CompaniesGroupsBase):
    pass


class CompaniesGroups(CompaniesGroupsBase):
    id: int

    class Config:
        orm_mode = True
