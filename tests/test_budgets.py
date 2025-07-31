def test_budget_crud(client):
    # Create a new budget entry
    budget_data = {
        "fiscal_year": 2021,
        "fund_code": "FC100",
        "program_code": "PC200",
        "account": "AC300",
        "deptid": "D400",
        "operating_unit": "OU500",
        "class": "CL600",
        "project_id": "PJ700",
        "budget_amount": 1000.50,
        "descr": "Initial budget",
    }
    response = client.post("/budgets/", json=budget_data)
    assert response.status_code == 201
    created = response.json()
    for field, value in budget_data.items():
        assert created[field] == value
    assert "id" in created
    budget_id = created["id"]

    # Retrieve the budget entry
    response = client.get(f"/budgets/{budget_id}")
    assert response.status_code == 200
    assert response.json() == created

    # List budgets
    response = client.get("/budgets/")
    assert response.status_code == 200
    budgets = response.json()
    assert isinstance(budgets, list)
    assert any(b["id"] == budget_id for b in budgets)

    # Update the budget entry
    update_data = budget_data.copy()
    update_data["descr"] = "Updated budget"
    response = client.put(f"/budgets/{budget_id}", json=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["descr"] == "Updated budget"

    # Delete the budget entry
    response = client.delete(f"/budgets/{budget_id}")
    assert response.status_code == 200
    deleted = response.json()
    assert deleted["id"] == budget_id

    # Confirm deletion
    response = client.get(f"/budgets/{budget_id}")
    assert response.status_code == 404


def test_default_ui_shows_only_latest_fiscal_year(client):
    # Create two budgets in different fiscal years
    older = {
        "fiscal_year": 2019,
        "fund_code": "FC_old",
        "program_code": "PC_old",
        "account": "AC_old",
        "deptid": "D_old",
        "operating_unit": "OU_old",
        "class": "CL_old",
        "project_id": "PJ_old",
        "budget_amount": 50.0,
        "descr": "Old year",
    }
    newer = older.copy()
    newer.update({
        "fiscal_year": 2021,
        "fund_code": "FC_new",
        "program_code": "PC_new",
        "account": "AC_new",
        "deptid": "D_new",
        "operating_unit": "OU_new",
        "class": "CL_new",
        "project_id": "PJ_new",
        "budget_amount": 75.0,
        "descr": "New year",
    })
    r1 = client.post("/budgets/", json=older)
    assert r1.status_code == 201
    r2 = client.post("/budgets/", json=newer)
    assert r2.status_code == 201

    # GET the default UI index (non-HTMX) should show only the newer row
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "New year" in html
    assert "Old year" not in html