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

    @router.get("/construction_budgets", response_class=HTMLResponse)
    def construction_index(request: Request, db: Session = Depends(get_db)):
        params = request.query_params
        is_htmx = bool(request.headers.get("hx-request"))
        has_filter = any(v for v in params.values())
        cons_budgets = crud.get_construction_budgets(db, skip=0, limit=None)
        bp = params.get("budget_period")
        if bp:
            bp_value = bp.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.budget_period and bp_value in str(b.budget_period).lower()
            ]
        fc = params.get("fund_code")
        if fc:
            fc_value = fc.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.fund_code and fc_value in str(b.fund_code).lower()
            ]
        pc = params.get("program_code")
        if pc:
            pc_value = pc.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.program_code and pc_value in str(b.program_code).lower()
            ]
        pid = params.get("project_id")
        if pid:
            pid_value = pid.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.project_id and pid_value in str(b.project_id).lower()
            ]
        aid = params.get("activity_id")
        if aid:
            aid_value = aid.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.activity_id and aid_value in str(b.activity_id).lower()
            ]
        la = params.get("line_descr")
        if la:
            la_value = la.lower()
            cons_budgets = [
                b
                for b in cons_budgets
                if b.line_descr and la_value in str(b.line_descr).lower()
            ]
        ma = params.get("monetary_amount")
        if ma:
            try:
                cons_budgets = [b for b in cons_budgets if b.monetary_amount == float(ma)]
            except ValueError:
                pass

        template_name = "construction_budget_rows.html" if (is_htmx or has_filter) else "construction_index.html"
        return templates.TemplateResponse(
            template_name, {"request": request, "construction_budgets": cons_budgets}
        )

    @router.post("/construction_budgets", response_class=HTMLResponse)
    def create_construction_budget_ui(
        request: Request,
        budget_period: str = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        project_id: str = Form(...),
        activity_id: str = Form(...),
        line_descr: str = Form(None),
        monetary_amount: float = Form(...),
        db: Session = Depends(get_db),
    ):
        cons_in = schemas.ConstructionBudgetCreate(
            budget_period=budget_period,
            fund_code=fund_code,
            program_code=program_code,
            project_id=project_id,
            activity_id=activity_id,
            line_descr=line_descr,
            monetary_amount=monetary_amount,
        )
        cons = crud.create_construction_budget(db, cons_in)
        return templates.TemplateResponse(
            "construction_budget_row.html", {"request": request, "budget": cons}
        )

    @router.get("/construction_budgets/{construction_budget_id}/edit", response_class=HTMLResponse)
    def edit_construction_budget_ui(request: Request, construction_budget_id: int, db: Session = Depends(get_db)):
        cons = crud.get_construction_budget(db, construction_budget_id)
        return templates.TemplateResponse(
            "construction_budget_edit_row.html", {"request": request, "budget": cons}
        )

    @router.get("/construction_budgets/{construction_budget_id}/cancel", response_class=HTMLResponse)
    def cancel_edit_construction_budget_ui(request: Request, construction_budget_id: int, db: Session = Depends(get_db)):
        cons = crud.get_construction_budget(db, construction_budget_id)
        return templates.TemplateResponse(
            "construction_budget_row.html", {"request": request, "budget": cons}
        )

    @router.put("/construction_budgets/{construction_budget_id}", response_class=HTMLResponse)
    def update_construction_budget_ui(
        request: Request,
        construction_budget_id: int,
        budget_period: str = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        project_id: str = Form(...),
        activity_id: str = Form(...),
        line_descr: str = Form(None),
        monetary_amount: float = Form(...),
        db: Session = Depends(get_db),
    ):
        cons_in = schemas.ConstructionBudgetCreate(
            budget_period=budget_period,
            fund_code=fund_code,
            program_code=program_code,
            project_id=project_id,
            activity_id=activity_id,
            line_descr=line_descr,
            monetary_amount=monetary_amount,
        )
        cons = crud.update_construction_budget(db, construction_budget_id, cons_in)
        return templates.TemplateResponse(
            "construction_budget_row.html", {"request": request, "budget": cons}
        )

    @router.delete("/construction_budgets/{construction_budget_id}", response_class=HTMLResponse)
    def delete_construction_budget_ui(request: Request, construction_budget_id: int, db: Session = Depends(get_db)):
        crud.delete_construction_budget(db, construction_budget_id)
        return HTMLResponse("")

    @router.get("/construction_budgets/bulk_upload", response_class=HTMLResponse)
    def construction_bulk_upload_form(request: Request):
        return templates.TemplateResponse("construction_bulk_upload_form.html", {"request": request})

    @router.post("/construction_budgets/bulk_upload/preview", response_class=HTMLResponse)
    def construction_bulk_upload_preview(request: Request, file: UploadFile = File(...)):
        df = pd.read_excel(file.file, dtype=str)
        df.columns = [str(col).strip().lower() for col in df.columns]
        if "fund_code" in df.columns:
            df["fund_code"] = df["fund_code"].apply(lambda x: x.zfill(2) if isinstance(x, str) else x)
        if "program_code" in df.columns:
            df["program_code"] = df["program_code"].apply(lambda x: x.zfill(4) if isinstance(x, str) else x)
        df.fillna("", inplace=True)
        rows = df.to_dict(orient="records")
        headers = list(df.columns)
        return templates.TemplateResponse(
            "construction_bulk_upload_preview.html",
            {"request": request, "headers": headers, "rows": rows},
        )

    @router.post("/construction_budgets/bulk_upload", response_class=HTMLResponse)
    def construction_bulk_upload(request: Request, rows_json: str = Form(...), db: Session = Depends(get_db)):
        rows = json.loads(rows_json)
        created = []
        for row in rows:
            cons_in = schemas.ConstructionBudgetCreate.model_validate(row)
            cons = crud.create_construction_budget(db, cons_in)
            created.append(cons)
        return templates.TemplateResponse(
            "construction_budget_rows.html", {"request": request, "construction_budgets": created}
        )

    @router.get("/construction_budgets/bulk_upload/cancel", response_class=HTMLResponse)
    def construction_bulk_upload_cancel(request: Request):
        return HTMLResponse("")

except ImportError:
    pass
