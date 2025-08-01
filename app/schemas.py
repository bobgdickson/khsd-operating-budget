from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,  # same as allow_population_by_field_name
    }

class OperatingBudgetCreate(OperatingBudgetBase):
    pass

class OperatingBudget(OperatingBudgetBase):
    id: int

class SupplierBudgetBase(BaseModel):
    vendor_id: Optional[str] = None
    descr: Optional[str] = None
    fiscal_year: str
    fund_code: str
    program_code: str
    account: str
    deptid: str
    operating_unit: str
    project_id: Optional[str] = None
    business_unit: Optional[str] = None
    amount: float

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }

class SupplierBudgetCreate(SupplierBudgetBase):
    pass

class SupplierBudget(SupplierBudgetBase):
    id: int
