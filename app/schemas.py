from pydantic import BaseModel, Field

class OperatingBudgetBase(BaseModel):
    fiscal_year: int
    fund_code: str
    program_code: str
    account: str
    deptid: str
    operating_unit: str
    class_: str = Field(..., alias="class")
    project_id: str
    budget_amount: float
    descr: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class OperatingBudgetCreate(OperatingBudgetBase):
    pass

class OperatingBudget(OperatingBudgetBase):
    id: int