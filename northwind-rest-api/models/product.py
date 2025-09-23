# models/product.py
from config import db

class Product(db.Model):
    __tablename__ = "Products"

    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String, nullable=False)
    SupplierID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer)
    QuantityPerUnit = db.Column(db.String)
    UnitPrice = db.Column(db.Float)
    UnitsInStock = db.Column(db.Integer)
    UnitsOnOrder = db.Column(db.Integer)
    ReorderLevel = db.Column(db.Integer)
    Discontinued = db.Column(db.Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
