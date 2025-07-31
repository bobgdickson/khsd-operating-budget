import io
import json

import pytest
pd = pytest.importorskip("pandas")
pytest.importorskip("openpyxl")


def test_bulk_upload_form_and_cancel(client):
    # GET the bulk-upload form fragment
    response = client.get("/budgets/bulk_upload")
    assert response.status_code == 200
    assert '<form id="bulk-upload-form"' in response.text

    # GET cancel clears the container
    response = client.get("/budgets/bulk_upload/cancel")
    assert response.status_code == 200
    assert response.text == ""


def test_bulk_upload_preview_and_confirm(client):
    # Prepare an in-memory Excel file with a single row matching the model headers
    df = pd.DataFrame([
        {
            "fiscal_year": 2022,
            "fund_code": "F1",
            "program_code": "P1",
            "account": "A1",
            "deptid": "D1",
            "operating_unit": "OU",
            "class": "CL",
            "project_id": "PJ",
            "budget_amount": 123.45,
            "descr": "Desc",
        }
    ])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)

    # POST to preview endpoint
    response = client.post(
        "/budgets/bulk_upload/preview",
        files={"file": ("test.xlsx", buf, 
                         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == 200
    text = response.text
    # Headers should be rendered from columns
    assert "<th>fiscal_year</th>" in text
    assert "<th>descr</th>" in text

    # Extract the hidden JSON payload
    tag = '<textarea name="rows_json" hidden>'
    start = text.find(tag)
    assert start != -1
    start += len(tag)
    end = text.find("</textarea>", start)
    rows_json = text[start:end]
    rows = json.loads(rows_json)
    assert isinstance(rows, list) and len(rows) == 1
    assert rows[0]["descr"] == "Desc"

    # POST to confirm/upload endpoint
    response2 = client.post(
        "/budgets/bulk_upload",
        data={"rows_json": rows_json},
    )
    assert response2.status_code == 200
    html2 = response2.text
    # Confirm that the new row appears in the table
    assert "Desc" in html2
    assert "123.45" in html2
    assert 'id="budget-' in html2