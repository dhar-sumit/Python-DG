# tests/test_customers.py
import json

def test_list_customers(client, sample_customer):
    resp = client.get("/customers/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert any(c["CustomerID"] == sample_customer.CustomerID for c in data)

def test_get_customer(client, sample_customer):
    resp = client.get(f"/customers/{sample_customer.CustomerID}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["CustomerID"] == sample_customer.CustomerID
    assert data["CompanyName"] == "Test Company"

    # confirm invalid customer
    invalid_customer = "invalid"
    resp2 = client.get(f"/customers/{invalid_customer}")
    assert resp2.status_code == 404

def test_create_customer(client):
    new_customer = {
        "CustomerID": "NEWTEST1",
        "CompanyName": "New Test Company",
        "ContactName": "New Test Name"
    }
    resp = client.post("/customers/", data=json.dumps(new_customer),
                       content_type="application/json")
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["CustomerID"] == "NEWTEST1"

    # Duplicate ID (manually setting ID)
    duplicate_customer = {
        "CustomerID": data["CustomerID"],
        "CompanyName": "Dup Company",
        "ContactName": "Dup Contact"
    }

    resp2 = client.post(
        "/customers/",
        data=json.dumps(duplicate_customer),
        content_type="application/json"
    )
    assert resp2.status_code == 409

    # Invalid payload
    invalid_customer = {"CustomerName": ""}
    resp3 = client.post(
        "/customers/",
        data=json.dumps(invalid_customer),
        content_type="application/json"
    )
    assert resp3.status_code == 400

    
def test_update_customer(client, sample_customer):
    update_data = {
        "CompanyName": "Updated Test Company"
    }
    resp = client.put(f"/customers/{sample_customer.CustomerID}",
                      data=json.dumps(update_data),
                      content_type="application/json")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["CompanyName"] == "Updated Test Company"

    # Invalid CustomerID
    invalid_customerID = "Invalid123"
    resp2 = client.put(
        f"/customers/{invalid_customerID}",
        data=json.dumps(update_data),
        content_type="application/json"
    )
    assert resp2.status_code == 404

    # Invalid payload
    invalid_customer = {"CustomerName": ""}
    resp3 = client.put(
        f"/customers/{sample_customer.CustomerID}",
        data=json.dumps(invalid_customer),
        content_type="application/json"
    )
    assert resp3.status_code == 400

def test_delete_customer(client, sample_customer):
    resp = client.delete(f"/customers/{sample_customer.CustomerID}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "deleted" in data["message"]

    # confirm deletion
    resp2 = client.get(f"/products/{sample_customer.CustomerID}")
    assert resp2.status_code == 404

    # Invalid CustomerID
    invalid_customerID = "Invalid123"
    resp2 = client.delete(f"/customers/{invalid_customerID}")
    assert resp2.status_code == 404

