from fastapi import APIRouter

router = APIRouter()

try:
    from fastapi import Depends, Request, Form, UploadFile, File
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from sqlalchemy.orm import Session
    import pandas as pd
    import json

    from app import crud, schemas
    from app.database import get_db

    templates = Jinja2Templates(directory="app/templates")

    @router.get("/", response_class=HTMLResponse)
    def index(request: Request, db: Session = Depends(get_db)):
        params = request.query_params
        is_htmx = bool(request.headers.get("hx-request"))
        has_filter = any(v for v in params.values())

        if not is_htmx and not has_filter:
            from sqlalchemy import func
            from app.models import OperatingBudget

            latest_year = db.query(func.max(OperatingBudget.fiscal_year)).scalar()
            if latest_year is not None:
                budgets = (
                    db.query(OperatingBudget)
                    .filter(OperatingBudget.fiscal_year == latest_year)
                    .order_by(OperatingBudget.id)
                    .all()
                )
            else:
                budgets = []
            return templates.TemplateResponse(
                "index.html", {"request": request, "budgets": budgets}
            )

        budgets = crud.get_budgets(db, skip=0, limit=None)
        fy = params.get("fiscal_year")
        if fy:
            budgets = [b for b in budgets if fy in str(b.fiscal_year)]
        fc = params.get("fund_code")
        if fc:
            budgets = [b for b in budgets if fc.lower() in b.fund_code.lower()]
        pc = params.get("program_code")
        if pc:
            budgets = [b for b in budgets if pc.lower() in b.program_code.lower()]
        ac = params.get("account")
        if ac:
            budgets = [b for b in budgets if ac.lower() in b.account.lower()]
        did = params.get("deptid")
        if did:
            budgets = [b for b in budgets if did.lower() in b.deptid.lower()]
        ou = params.get("operating_unit")
        if ou:
            budgets = [b for b in budgets if ou.lower() in b.operating_unit.lower()]
        cl = params.get("class")
        if cl:
            budgets = [b for b in budgets if cl.lower() in b.class_.lower()]
        pid = params.get("project_id")
        if pid:
            budgets = [b for b in budgets if pid.lower() in b.project_id.lower()]
        ba = params.get("budget_amount")
        if ba:
            try:
                budgets = [b for b in budgets if b.budget_amount == float(ba)]
            except ValueError:
                pass
        ds = params.get("descr")
        if ds:
            budgets = [b for b in budgets if ds.lower() in b.descr.lower()]

        template_name = "budget_rows.html" if (is_htmx or has_filter) else "index.html"
        return templates.TemplateResponse(
            template_name, {"request": request, "budgets": budgets}
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

    @router.get("/budgets/bulk_upload", response_class=HTMLResponse)
    def bulk_upload_form(request: Request):
        return templates.TemplateResponse("bulk_upload_form.html", {"request": request})

    @router.post("/budgets/bulk_upload/preview", response_class=HTMLResponse)
    def bulk_upload_preview(request: Request, file: UploadFile = File(...)):
        df = pd.read_excel(file.file, dtype=str)
        df.columns = [str(col).strip().lower() for col in df.columns]
        df = df.rename(columns={"class": "class_"})
        if "fund_code" in df.columns:
            df["fund_code"] = df["fund_code"].apply(lambda x: x.zfill(2) if isinstance(x, str) else x)
        if "program_code" in df.columns:
            df["program_code"] = df["program_code"].apply(lambda x: x.zfill(4) if isinstance(x, str) else x)
        df.fillna("", inplace=True)
        rows = df.to_dict(orient="records")
        headers = list(df.columns)
        rows_json = json.dumps(rows)
        return templates.TemplateResponse(
            "bulk_upload_preview.html",
            {"request": request, "headers": headers, "rows": rows, "rows_json": rows_json},
        )

    @router.post("/budgets/bulk_upload", response_class=HTMLResponse)
    def bulk_upload(request: Request, rows_json: str = Form(...), db: Session = Depends(get_db)):
        rows = json.loads(rows_json)
        created = []
        for row in rows:
            if "class" in row:
                row["class_"] = row.pop("class")
            budget_in = schemas.OperatingBudgetCreate.model_validate(row)
            budget = crud.create_budget(db, budget_in)
            created.append(budget)
        return templates.TemplateResponse(
            "budget_rows.html", {"request": request, "budgets": created}
        )

    @router.get("/budgets/bulk_upload/cancel", response_class=HTMLResponse)
    def bulk_upload_cancel(request: Request):
        return HTMLResponse("")

except ImportError:
    pass
