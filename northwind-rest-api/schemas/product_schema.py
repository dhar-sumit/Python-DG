# schemas/customer_schema.py
from pydantic import BaseModel

class ProductSchema(BaseModel):
    ProductID: int
    ProductName: str
    SupplierID: int | None = None
    CategoryID: int | None = None
    QuantityPerUnit: str | None = None
    UnitPrice: float | None = None
    UnitsInStock: int | None = None
    UnitsOnOrder: int | None = None
    ReorderLevel: int | None = None
    Discontinued: int | None = None
