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

    @router.get("/supplier_budgets", response_class=HTMLResponse)
    def supplier_index(request: Request, db: Session = Depends(get_db)):
        params = request.query_params
        is_htmx = bool(request.headers.get("hx-request"))
        has_filter = any(v for v in params.values())

        if not is_htmx and not has_filter:
            from sqlalchemy import func
            from app.models import SupplierBudget

            latest_year = db.query(func.max(SupplierBudget.fiscal_year)).scalar()
            if latest_year is not None:
                sup_budgets = (
                    db.query(SupplierBudget)
                    .filter(SupplierBudget.fiscal_year == latest_year)
                    .order_by(SupplierBudget.id)
                    .all()
                )
            else:
                sup_budgets = []
            return templates.TemplateResponse(
                "supplier_index.html", {"request": request, "supplier_budgets": sup_budgets}
            )

        sup_budgets = crud.get_supplier_budgets(db, skip=0, limit=None)
        fy = params.get("fiscal_year")
        if fy:
            sup_budgets = [b for b in sup_budgets if fy in str(b.fiscal_year)]
        fc = params.get("fund_code")
        if fc:
            sup_budgets = [b for b in sup_budgets if fc.lower() in b.fund_code.lower()]
        pc = params.get("program_code")
        if pc:
            sup_budgets = [b for b in sup_budgets if pc.lower() in b.program_code.lower()]
        ac = params.get("account")
        if ac:
            sup_budgets = [b for b in sup_budgets if ac.lower() in b.account.lower()]
        did = params.get("deptid")
        if did:
            sup_budgets = [b for b in sup_budgets if did.lower() in b.deptid.lower()]
        ou = params.get("operating_unit")
        if ou:
            sup_budgets = [b for b in sup_budgets if ou.lower() in b.operating_unit.lower()]
        pid = params.get("project_id")
        if pid:
            sup_budgets = [b for b in sup_budgets if b.project_id and pid.lower() in b.project_id.lower()]
        bu = params.get("business_unit")
        if bu:
            sup_budgets = [b for b in sup_budgets if b.business_unit and bu.lower() in b.business_unit.lower()]
        vid = params.get("vendor_id")
        if vid:
            sup_budgets = [b for b in sup_budgets if b.vendor_id and vid.lower() in b.vendor_id.lower()]
        amt = params.get("amount")
        if amt:
            try:
                sup_budgets = [b for b in sup_budgets if b.amount == float(amt)]
            except ValueError:
                pass
        ds = params.get("descr")
        if ds:
            sup_budgets = [b for b in sup_budgets if b.descr and ds.lower() in b.descr.lower()]

        template_name = "supplier_budget_rows.html" if (is_htmx or has_filter) else "supplier_index.html"
        return templates.TemplateResponse(
            template_name, {"request": request, "supplier_budgets": sup_budgets}
        )

    @router.post("/supplier_budgets", response_class=HTMLResponse)
    def create_supplier_budget_ui(
        request: Request,
        vendor_id: str = Form(None),
        descr: str = Form(None),
        fiscal_year: str = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        account: str = Form(...),
        deptid: str = Form(...),
        operating_unit: str = Form(...),
        project_id: str = Form(None),
        business_unit: str = Form(None),
        amount: float = Form(...),
        db: Session = Depends(get_db),
    ):
        supplier_in = schemas.SupplierBudgetCreate(
            vendor_id=vendor_id,
            descr=descr,
            fiscal_year=fiscal_year,
            fund_code=fund_code,
            program_code=program_code,
            account=account,
            deptid=deptid,
            operating_unit=operating_unit,
            project_id=project_id,
            business_unit=business_unit,
            amount=amount,
        )
        sup = crud.create_supplier_budget(db, supplier_in)
        return templates.TemplateResponse(
            "supplier_budget_row.html", {"request": request, "budget": sup}
        )

    @router.get("/supplier_budgets/{supplier_budget_id}/edit", response_class=HTMLResponse)
    def edit_supplier_budget_ui(request: Request, supplier_budget_id: int, db: Session = Depends(get_db)):
        sup = crud.get_supplier_budget(db, supplier_budget_id)
        return templates.TemplateResponse(
            "supplier_budget_edit_row.html", {"request": request, "budget": sup}
        )

    @router.get("/supplier_budgets/{supplier_budget_id}/cancel", response_class=HTMLResponse)
    def cancel_edit_supplier_budget_ui(request: Request, supplier_budget_id: int, db: Session = Depends(get_db)):
        sup = crud.get_supplier_budget(db, supplier_budget_id)
        return templates.TemplateResponse(
            "supplier_budget_row.html", {"request": request, "budget": sup}
        )

    @router.put("/supplier_budgets/{supplier_budget_id}", response_class=HTMLResponse)
    def update_supplier_budget_ui(
        request: Request,
        supplier_budget_id: int,
        vendor_id: str = Form(None),
        descr: str = Form(None),
        fiscal_year: str = Form(...),
        fund_code: str = Form(...),
        program_code: str = Form(...),
        account: str = Form(...),
        deptid: str = Form(...),
        operating_unit: str = Form(...),
        project_id: str = Form(None),
        business_unit: str = Form(None),
        amount: float = Form(...),
        db: Session = Depends(get_db),
    ):
        supplier_in = schemas.SupplierBudgetCreate(
            vendor_id=vendor_id,
            descr=descr,
            fiscal_year=fiscal_year,
            fund_code=fund_code,
            program_code=program_code,
            account=account,
            deptid=deptid,
            operating_unit=operating_unit,
            project_id=project_id,
            business_unit=business_unit,
            amount=amount,
        )
        sup = crud.update_supplier_budget(db, supplier_budget_id, supplier_in)
        return templates.TemplateResponse(
            "supplier_budget_row.html", {"request": request, "budget": sup}
        )

    @router.delete("/supplier_budgets/{supplier_budget_id}", response_class=HTMLResponse)
    def delete_supplier_budget_ui(request: Request, supplier_budget_id: int, db: Session = Depends(get_db)):
        crud.delete_supplier_budget(db, supplier_budget_id)
        return HTMLResponse("")

    @router.get("/supplier_budgets/bulk_upload", response_class=HTMLResponse)
    def supplier_bulk_upload_form(request: Request):
        return templates.TemplateResponse("supplier_bulk_upload_form.html", {"request": request})

    @router.post("/supplier_budgets/bulk_upload/preview", response_class=HTMLResponse)
    def supplier_bulk_upload_preview(request: Request, file: UploadFile = File(...)):
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
            "supplier_bulk_upload_preview.html",
            {"request": request, "headers": headers, "rows": rows},
        )

    @router.post("/supplier_budgets/bulk_upload", response_class=HTMLResponse)
    def supplier_bulk_upload(request: Request, rows_json: str = Form(...), db: Session = Depends(get_db)):
        rows = json.loads(rows_json)
        created = []
        for row in rows:
            sup_in = schemas.SupplierBudgetCreate.model_validate(row)
            sup = crud.create_supplier_budget(db, sup_in)
            created.append(sup)
        return templates.TemplateResponse(
            "supplier_budget_rows.html", {"request": request, "supplier_budgets": created}
        )

    @router.get("/supplier_budgets/bulk_upload/cancel", response_class=HTMLResponse)
    def supplier_bulk_upload_cancel(request: Request):
        return HTMLResponse("")

except ImportError:
    pass
