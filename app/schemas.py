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
    vendor_id: str
    name: str
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,  # same as allow_population_by_field_name
    }

class OperatingBudgetCreate(OperatingBudgetBase):
    pass

class OperatingBudget(OperatingBudgetBase):
    id: int