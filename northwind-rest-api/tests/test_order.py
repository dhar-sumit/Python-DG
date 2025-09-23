# tests/test_order.py
import json

def test_list_orders(client, sample_order):
    resp = client.get("/orders/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(o["OrderID"] == sample_order.OrderID for o in data)

def test_get_order(client, sample_order):
    resp = client.get(f"/orders/{sample_order.OrderID}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["OrderID"] == sample_order.OrderID
    assert data["CustomerID"] == sample_order.CustomerID

def test_create_order(client, sample_customer):
    new_order = {
        "OrderID": 2,
        "CustomerID": sample_customer.CustomerID,
        "EmployeeID": 2,
    }
    resp = client.post("/orders/", data=json.dumps(new_order), content_type="application/json")
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["OrderID"] == new_order["OrderID"]
    assert data["CustomerID"] == new_order["CustomerID"]

    # Duplicate ID (manually setting ID)
    resp2 = client.post("/orders/", data=json.dumps(new_order), content_type="application/json")

    assert resp2.status_code == 409

    # Invalid payload
    invalid_order = {"OrderID": None}
    resp3 = client.post(
        "/orders/", 
        data=json.dumps(invalid_order), 
        content_type="application/json"
    )

    assert resp3.status_code == 400


def test_update_order(client, sample_order):
    update_data = {
        "OrderID": sample_order.OrderID,
        "CustomerID": sample_order.CustomerID,
        "EmployeeID": 99,        
        "Freight": 50.0,
    }
    resp = client.put(f"/orders/{sample_order.OrderID}", data=json.dumps(update_data), content_type="application/json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["EmployeeID"] == 99
    assert data["Freight"] == 50.0

    # Invalid order
    invalid_orderID = 999999999
    resp2 = client.put(f"/orders/{invalid_orderID}", data=json.dumps(update_data), content_type="application/json")
    assert resp2.status_code == 404

    # Invalid payload
    invalid_order = {
        "CustomerID": sample_order.CustomerID,  # valid
        "EmployeeID": "not-an-int"  # invalid type
    }
    resp3 = client.put(
        f"/orders/{sample_order.OrderID}", 
        data=json.dumps(invalid_order), 
        content_type="application/json"
    )

    assert resp3.status_code == 400

def test_delete_order(client, sample_order):
    resp = client.delete(f"/orders/{sample_order.OrderID}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert f"{sample_order.OrderID}" in data["message"]

    # Confirm deletion
    resp2 = client.get(f"/orders/{sample_order.OrderID}")
    assert resp2.status_code == 404

    # Invalid order
    invalid_orderID = 999999999
    resp2 = client.delete(f"/orders/{invalid_orderID}")
    assert resp2.status_code == 404

def test_get_customer_orders(client, sample_order):
    customer_id = sample_order.CustomerID

    resp = client.get(f"/orders/customer/{customer_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert any(o["OrderID"] == sample_order.OrderID for o in data)

    invalid_customer_id = "Invalid123"
    resp2 = client.get(f"/orders/customer/{invalid_customer_id}")
    assert resp2.status_code == 404
