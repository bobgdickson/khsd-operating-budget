from sqlalchemy import Column, Integer, String, Float

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
    vendor_id = Column("VENDOR_ID", String, index=True)
    name = Column("NAME", String, index=True)