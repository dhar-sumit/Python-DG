# schemas/customer_schema.py
from pydantic import BaseModel

class CustomerSchema(BaseModel):
    CustomerID: str
    CompanyName: str
    ContactName: str | None = None
    ContactTitle: str | None = None
    Address: str | None = None
    City: str | None = None
    Region: str | None = None
    PostalCode: str | None = None
    Country: str | None = None
    Phone: str | None = None
    Fax: str | None = None
