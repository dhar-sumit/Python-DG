# tests/test_product.py
import json

def test_list_products(client, sample_product):
    resp = client.get("/products/")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert any(c["ProductID"] == sample_product.ProductID for c in data)

def test_get_product(client, sample_product):
    resp = client.get(f"/products/{sample_product.ProductID}")
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert data["ProductName"] == "Test Product"
    assert data["UnitPrice"] == 20.5

def test_create_product(client):
    new_product = {
        "ProductID": 79,
        "ProductName": "New Test Product",
        "QuantityPerUnit": "Test 20 boxes"
    }
    resp = client.post(
        "/products/",
        data=json.dumps(new_product),
        content_type="application/json"
    )
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["ProductName"] == new_product["ProductName"]
    assert data["QuantityPerUnit"] == new_product["QuantityPerUnit"]

    # Invalid payload
    invalid_product = {"ProductID": "Invalid123"}
    resp2 = client.post(
        "/products/",
        data=json.dumps(invalid_product),
        content_type="application/json"
    )
    assert resp2.status_code == 400

    # Duplicate product
    resp3 = client.post(
        "/products/",
        data=json.dumps(new_product),
        content_type="application/json"
    )
    assert resp3.status_code == 409

def test_update_product(client, sample_product):
    update_data = {
        "ProductName": "Updated Test Product",
        "UnitPrice": 100.85,
        "UnitsInStock": 87,
    }
    resp = client.put(
        f"/products/{sample_product.ProductID}",
        data=json.dumps(update_data),
        content_type="application/json"
    )
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["ProductName"] == update_data["ProductName"]
    assert data["UnitPrice"] == update_data["UnitPrice"]
    assert data["UnitsInStock"] == update_data["UnitsInStock"]

    # Invalid product
    invalid_productID = 999999999
    resp = client.put(
        f"/products/{invalid_productID}",
        data=json.dumps(update_data),
        content_type="application/json"
    )
    assert resp.status_code == 404

    # Invalid payload
    invalid_product = {"ProductID": "Invalid123"}
    resp3 = client.put(
        f"/products/{sample_product.ProductID}",
        data=json.dumps(invalid_product),
        content_type="application/json"
    )
    assert resp3.status_code == 400

def test_delete_product(client, sample_product):
    resp = client.delete(f"/products/{sample_product.ProductID}")
    assert resp.status_code == 200
    
    data = resp.get_json()
    assert "deleted" in data["message"]

    # confirm deletion
    resp2 = client.get(f"/products/{sample_product.ProductID}")
    assert resp2.status_code == 404

    # Invalid product
    invalid_productID = 999999999
    resp = client.delete(f"/products/{invalid_productID}")
    assert resp.status_code == 404
