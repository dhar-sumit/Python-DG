# models/order.py
from config import db

class Order(db.Model):
    __tablename__ = "orders"

    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.String, db.ForeignKey("customers.CustomerID"))
    EmployeeID = db.Column(db.Integer)
    OrderDate = db.Column(db.DateTime)
    RequiredDate = db.Column(db.DateTime)
    ShippedDate = db.Column(db.DateTime)
    ShipVia = db.Column(db.Integer)
    Freight = db.Column(db.Float)
    ShipName = db.Column(db.String)
    ShipAddress = db.Column(db.String)
    ShipCity = db.Column(db.String)
    ShipRegion = db.Column(db.String)
    ShipPostalCode = db.Column(db.String)
    ShipCountry = db.Column(db.String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
