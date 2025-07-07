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