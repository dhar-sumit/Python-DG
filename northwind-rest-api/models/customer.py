# models/customer.py
from config import db

class Customer(db.Model):
    __tablename__ = "customers"

    CustomerID = db.Column(db.String(10), primary_key=True)
    CompanyName = db.Column(db.String)
    ContactName = db.Column(db.String)
    ContactTitle = db.Column(db.String)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    Region = db.Column(db.String)
    PostalCode = db.Column(db.String)
    Country = db.Column(db.String)
    Phone = db.Column(db.String)
    Fax = db.Column(db.String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
