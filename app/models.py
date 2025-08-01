from sqlalchemy import Column, Integer, String, Float, Numeric

from .database import Base

class OperatingBudget(Base):
    __tablename__ = "OPERATING_BUDGET"

    id = Column("ID", Integer, primary_key=True, index=True)
    fiscal_year = Column("FISCAL_YEAR", Integer, index=True)
    fund_code = Column("FUND_CODE", String, index=True)
    program_code = Column("PROGRAM_CODE", String, index=True)
    account = Column("ACCOUNT", String, index=True)
    deptid = Column("DEPTID", String, index=True)
    operating_unit = Column("OPERATING_UNIT", String, index=True)
    class_ = Column("CLASS", String, index=True)
    project_id = Column("PROJECT_ID", String, index=True)
    budget_amount = Column("BUDGET_AMOUNT", Float)
    descr = Column("DESCR", String, index=True)

class SupplierBudget(Base):
    __tablename__ = "SUPPLIER_BUDGET"

    id = Column("ID", Integer, primary_key=True, index=True)
    vendor_id = Column("VENDOR_ID", String(15), nullable=True)
    descr = Column("DESCR", String(120), nullable=True)
    fiscal_year = Column("FISCAL_YEAR", String(4), nullable=True, index=True)
    fund_code = Column("FUND_CODE", String(4), nullable=True, index=True)
    program_code = Column("PROGRAM_CODE", String(4), nullable=True, index=True)
    account = Column("ACCOUNT", String(10), nullable=True, index=True)
    operating_unit = Column("OPERATING_UNIT", String(4), nullable=True, index=True)
    deptid = Column("DEPTID", String(10), nullable=True, index=True)
    project_id = Column("PROJECT_ID", String(26), nullable=True, index=True)
    business_unit = Column("BUSINESS_UNIT", String(5), nullable=True, index=True)
    amount = Column("AMOUNT", Numeric(10, 2), nullable=True)