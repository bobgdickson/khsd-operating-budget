from sqlalchemy.orm import Session

from . import models, schemas

def get_budget(db: Session, budget_id: int):
    return db.query(models.OperatingBudget).filter(models.OperatingBudget.id == budget_id).first()

from typing import Optional

def get_budgets(db: Session, skip: int = 0, limit: Optional[int] = None):
    """
    Retrieve budgets with optional pagination. If limit is None, no LIMIT clause is applied.
    """
    query = db.query(models.OperatingBudget).order_by(models.OperatingBudget.id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def create_budget(db: Session, budget: schemas.OperatingBudgetCreate):
    db_budget = models.OperatingBudget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, budget: schemas.OperatingBudgetCreate):
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return None
    for key, value in budget.dict().items():
        setattr(db_budget, key, value)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int):
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return None
    db.delete(db_budget)
    db.commit()
    return db_budget

def get_supplier_budget(db: Session, supplier_budget_id: int):
    return db.query(models.SupplierBudget).filter(models.SupplierBudget.id == supplier_budget_id).first()

def get_supplier_budgets(db: Session, skip: int = 0, limit: Optional[int] = None):
    """
    Retrieve supplier budgets with optional pagination. If limit is None, no LIMIT clause is applied.
    """
    query = db.query(models.SupplierBudget).order_by(models.SupplierBudget.id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def create_supplier_budget(db: Session, supplier_budget: schemas.SupplierBudgetCreate):
    db_supplier_budget = models.SupplierBudget(**supplier_budget.dict())
    db.add(db_supplier_budget)
    db.commit()
    db.refresh(db_supplier_budget)
    return db_supplier_budget

def update_supplier_budget(db: Session, supplier_budget_id: int, supplier_budget: schemas.SupplierBudgetCreate):
    db_supplier_budget = get_supplier_budget(db, supplier_budget_id)
    if not db_supplier_budget:
        return None
    for key, value in supplier_budget.dict().items():
        setattr(db_supplier_budget, key, value)
    db.commit()
    db.refresh(db_supplier_budget)
    return db_supplier_budget

def delete_supplier_budget(db: Session, supplier_budget_id: int):
    db_supplier_budget = get_supplier_budget(db, supplier_budget_id)
    if not db_supplier_budget:
        return None
    db.delete(db_supplier_budget)
    db.commit()
    return db_supplier_budget


def get_construction_budget(db: Session, construction_budget_id: int):
    return (
        db.query(models.ConstructionBudget)
        .filter(models.ConstructionBudget.id == construction_budget_id)
        .first()
    )


def get_construction_budgets(db: Session, skip: int = 0, limit: Optional[int] = None):
    query = db.query(models.ConstructionBudget).order_by(models.ConstructionBudget.id).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def create_construction_budget(db: Session, construction_budget: schemas.ConstructionBudgetCreate):
    db_obj = models.ConstructionBudget(**construction_budget.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_construction_budget(db: Session, construction_budget_id: int, construction_budget: schemas.ConstructionBudgetCreate):
    db_obj = get_construction_budget(db, construction_budget_id)
    if not db_obj:
        return None
    for key, value in construction_budget.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_construction_budget(db: Session, construction_budget_id: int):
    db_obj = get_construction_budget(db, construction_budget_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
