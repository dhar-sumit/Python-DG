# schemas/order_schema.py
from pydantic import BaseModel
from datetime import datetime

class OrderSchema(BaseModel):
    OrderID: int                     
    CustomerID: str | None = None
    EmployeeID: int | None = None
    OrderDate: datetime | None = None
    RequiredDate: datetime | None = None
    ShippedDate: datetime | None = None
    ShipVia: int | None = None
    Freight: float | None = 0
    ShipName: str | None = None
    ShipAddress: str | None = None
    ShipCity: str | None = None
    ShipRegion: str | None = None
    ShipPostalCode: str | None = None
    ShipCountry: str | None = None
