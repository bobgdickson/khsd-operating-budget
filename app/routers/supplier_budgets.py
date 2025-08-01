from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/supplier_budgets",
    tags=["supplier_budgets"],
)

@router.post("/", response_model=schemas.SupplierBudget, status_code=status.HTTP_201_CREATED)
def create_supplier_budget(supplier_budget: schemas.SupplierBudgetCreate, db: Session = Depends(get_db)):
    return crud.create_supplier_budget(db, supplier_budget)

@router.get("/", response_model=List[schemas.SupplierBudget])
def read_supplier_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orm_objs = crud.get_supplier_budgets(db, skip, limit)
    return [schemas.SupplierBudget.model_validate(obj) for obj in orm_objs]

@router.get("/{supplier_budget_id}", response_model=schemas.SupplierBudget)
def read_supplier_budget(supplier_budget_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_supplier_budget(db, supplier_budget_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="SupplierBudget not found")
    return db_obj

@router.put("/{supplier_budget_id}", response_model=schemas.SupplierBudget)
def update_supplier_budget(supplier_budget_id: int, supplier_budget: schemas.SupplierBudgetCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_supplier_budget(db, supplier_budget_id, supplier_budget)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="SupplierBudget not found")
    return db_obj

@router.delete("/{supplier_budget_id}", response_model=schemas.SupplierBudget)
def delete_supplier_budget(supplier_budget_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_supplier_budget(db, supplier_budget_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="SupplierBudget not found")
    return db_obj
