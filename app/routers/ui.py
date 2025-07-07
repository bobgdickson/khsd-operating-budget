from fastapi import APIRouter
from app import crud, schemas
from app.database import get_db

router = APIRouter()

try:
    from fastapi import Depends, Request, Form
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from sqlalchemy.orm import Session

    templates = Jinja2Templates(directory="app/templates")

    from typing import Optional
    from fastapi import Query

    @router.get("/", response_class=HTMLResponse)
    def index(
        request: Request,
        db: Session = Depends(get_db),
        fiscal_year: Optional[int] = Query(None),
        fund_code: Optional[str] = Query(None),
        program_code: Optional[str] = Query(None),
        account: Optional[str] = Query(None),
        deptid: Optional[str] = Query(None),
        operating_unit: Optional[str] = Query(None),
        class_: Optional[str] = Query(None, alias="class"),
        project_id: Optional[str] = Query(None),
        budget_amount: Optional[float] = Query(None),
        descr: Optional[str] = Query(None),
    ):
        budgets = crud.get_budgets(db, skip=0, limit=None)
        if fiscal_year is not None:
            budgets = [b for b in budgets if b.fiscal_year == fiscal_year]
        if fund_code:
            budgets = [b for b in budgets if fund_code.lower() in b.fund_code.lower()]
        if program_code:
            budgets = [b for b in budgets if program_code.lower() in b.program_code.lower()]
        if account:
            budgets = [b for b in budgets if account.lower() in b.account.lower()]
        if deptid:
            budgets = [b for b in budgets if deptid.lower() in b.deptid.lower()]
        if operating_unit:
            budgets = [b for b in budgets if operating_unit.lower() in b.operating_unit.lower()]
        if class_:
            budgets = [b for b in budgets if class_.lower() in b.class_.lower()]
        if project_id:
            budgets = [b for b in budgets if project_id.lower() in b.project_id.lower()]
        if budget_amount is not None:
            budgets = [b for b in budgets if b.budget_amount == budget_amount]
        if descr:
            budgets = [b for b in budgets if descr.lower() in b.descr.lower()]

        template = (
            "budget_rows.html"
            if request.headers.get("hx-request", False)
            else "index.html"
        )
        return templates.TemplateResponse(
            template, {"request": request, "budgets": budgets}
        )

    @router.post("/budgets", response_class=HTMLResponse)
    def create_budget_ui(
        request: Request,
        fiscal_year: int = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        account: str = Form(...),
        deptid: str = Form(...),
        operating_unit: str = Form(...),
        class_: str = Form(..., alias="class"),
        project_id: str = Form(...),
        budget_amount: float = Form(...),
        descr: str = Form(...),
        db: Session = Depends(get_db),
    ):
        budget_in = schemas.OperatingBudgetCreate(
            fiscal_year=fiscal_year,
            fund_code=fund_code,
            program_code=program_code,
            account=account,
            deptid=deptid,
            operating_unit=operating_unit,
            class_=class_,
            project_id=project_id,
            budget_amount=budget_amount,
            descr=descr,
        )
        budget = crud.create_budget(db, budget_in)
        return templates.TemplateResponse(
            "budget_row.html", {"request": request, "budget": budget}
        )

    @router.get("/budgets/{budget_id}/edit", response_class=HTMLResponse)
    def edit_budget_ui(request: Request, budget_id: int, db: Session = Depends(get_db)):
        budget = crud.get_budget(db, budget_id)
        return templates.TemplateResponse(
            "budget_edit_row.html", {"request": request, "budget": budget}
        )

    @router.get("/budgets/{budget_id}/cancel", response_class=HTMLResponse)
    def cancel_edit_budget_ui(request: Request, budget_id: int, db: Session = Depends(get_db)):
        budget = crud.get_budget(db, budget_id)
        return templates.TemplateResponse(
            "budget_row.html", {"request": request, "budget": budget}
        )

    @router.put("/budgets/{budget_id}", response_class=HTMLResponse)
    def update_budget_ui(
        request: Request,
        budget_id: int,
        fiscal_year: int = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        account: str = Form(...),
        deptid: str = Form(...),
        operating_unit: str = Form(...),
        class_: str = Form(..., alias="class"),
        project_id: str = Form(...),
        budget_amount: float = Form(...),
        descr: str = Form(...),
        db: Session = Depends(get_db),
    ):
        budget_in = schemas.OperatingBudgetCreate(
            fiscal_year=fiscal_year,
            fund_code=fund_code,
            program_code=program_code,
            account=account,
            deptid=deptid,
            operating_unit=operating_unit,
            class_=class_,
            project_id=project_id,
            budget_amount=budget_amount,
            descr=descr,
        )
        budget = crud.update_budget(db, budget_id, budget_in)
        return templates.TemplateResponse(
            "budget_row.html", {"request": request, "budget": budget}
        )

    @router.delete("/budgets/{budget_id}", response_class=HTMLResponse)
    def delete_budget_ui(request: Request, budget_id: int, db: Session = Depends(get_db)):
        crud.delete_budget(db, budget_id)
        return HTMLResponse("")
except ImportError:
    # Templating dependencies not available; skip UI routes
    pass