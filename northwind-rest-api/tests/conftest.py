# tests/conftest.py
import pytest
from app import create_app
from config import db
from models.customer import Customer
from models.order import Order
from models.product import Product
from datetime import datetime

@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for tests."""
    test_config = {
        "TESTING": True,
        # Override config to use in-memory DB
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }
    app = create_app(test_config)


    with app.app_context():
        db.create_all()  # Create tables in-memory
        yield app
        db.session.remove()
        db.drop_all()  # Clean up

@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_customer(app):
    """Add a sample customer to DB for tests."""
    c = Customer(
        CustomerID="TEST1",
        CompanyName="Test Company",
        ContactName="Test Name",
        ContactTitle="Test Manager",
        Address="Test Address",
        City="Test City",
        Region="Test Region",
        PostalCode="123456",
        Country="Test Country",
        Phone="1234567890",
        Fax="0987654321"
    )
    db.session.add(c)
    db.session.commit()
    yield c
    c = db.session.get(Customer, c.CustomerID)
    if c:
        db.session.delete(c)
        db.session.commit()

@pytest.fixture
def sample_product(app):
    p = Product(
        ProductID=78,
        ProductName="Test Product",
        SupplierID=1,
        CategoryID=1,
        QuantityPerUnit="Test 10 boxes",
        UnitPrice=20.5,
        UnitsInStock=15,
        UnitsOnOrder=5,
        ReorderLevel=3,
        Discontinued=0
    )
    db.session.add(p)
    db.session.commit()
    yield p
    p = db.session.get(Product, p.ProductID)
    if p:
        db.session.delete(p)
        db.session.commit()

@pytest.fixture
def sample_order(sample_customer):
    """Add a sample order linked to sample_customer."""
    o = Order(
        OrderID=1,
        CustomerID=sample_customer.CustomerID,
        EmployeeID=1,
        OrderDate=datetime.now(),
        RequiredDate=datetime.now(),
        ShippedDate=datetime.now(),
        ShipVia=1,
        Freight=10.0,
        ShipName="Test Ship",
        ShipAddress="Test Address",
        ShipCity="Test City",
        ShipRegion="Test Region",
        ShipPostalCode="123456",
        ShipCountry="Test Country"
    )
    db.session.add(o)
    db.session.commit()
    yield o
    o = db.session.get(Order, o.OrderID)
    if o:
        db.session.delete(o)
        db.session.commit()
