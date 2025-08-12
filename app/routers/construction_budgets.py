from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/construction_budgets",
    tags=["construction_budgets"],
)

@router.post("/", response_model=schemas.ConstructionBudget, status_code=status.HTTP_201_CREATED)
def create_construction_budget(construction_budget: schemas.ConstructionBudgetCreate, db: Session = Depends(get_db)):
    return crud.create_construction_budget(db, construction_budget)

@router.get("/", response_model=List[schemas.ConstructionBudget])
def read_construction_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orm_objs = crud.get_construction_budgets(db, skip, limit)
    return [schemas.ConstructionBudget.model_validate(obj) for obj in orm_objs]

@router.get("/{construction_budget_id}", response_model=schemas.ConstructionBudget)
def read_construction_budget(construction_budget_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_construction_budget(db, construction_budget_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="ConstructionBudget not found")
    return db_obj

@router.put("/{construction_budget_id}", response_model=schemas.ConstructionBudget)
def update_construction_budget(construction_budget_id: int, construction_budget: schemas.ConstructionBudgetCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_construction_budget(db, construction_budget_id, construction_budget)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="ConstructionBudget not found")
    return db_obj

@router.delete("/{construction_budget_id}", response_model=schemas.ConstructionBudget)
def delete_construction_budget(construction_budget_id: int, db: Session = Depends(get_db)):
    db_obj = crud.delete_construction_budget(db, construction_budget_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="ConstructionBudget not found")
    return db_obj
