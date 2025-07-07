from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
)

@router.post("/", response_model=schemas.OperatingBudget, status_code=status.HTTP_201_CREATED)
def create_budget(budget: schemas.OperatingBudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db, budget)

@router.get("/", response_model=List[schemas.OperatingBudget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orm_objs = crud.get_budgets(db, skip, limit)
    return [schemas.OperatingBudget.model_validate(obj) for obj in orm_objs]

@router.get("/{budget_id}", response_model=schemas.OperatingBudget)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = crud.get_budget(db, budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.put("/{budget_id}", response_model=schemas.OperatingBudget)
def update_budget(budget_id: int, budget: schemas.OperatingBudgetCreate, db: Session = Depends(get_db)):
    db_budget = crud.update_budget(db, budget_id, budget)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.delete("/{budget_id}", response_model=schemas.OperatingBudget)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = crud.delete_budget(db, budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget