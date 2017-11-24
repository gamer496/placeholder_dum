from app import db, app
from datetime import datetime


class QrCode(db.Model):
    __tablename__ = "qrcodes"
    id                          =db.Column      (db.Integer, primary_key = True)
    uid                         =db.Column      (db.String(250), unique = True, index = True)
    public_id                   =db.Column      (db.String(250))
    url                         =db.Column      (db.String(250), unique = True)
    created_on                  =db.Column      (db.DateTime())
    order_id                    =db.Column      (db.String(250), unique = True, index = True)
    associated_on               =db.Column      (db.DateTime())

    def __init__(self):
        self.created_on = datetime.utcnow()

    def set_associated_on(self):
        self.associated_on = datetime.utcnow()

    def serialize(self):
        d = {}
        d["url"] = self.url
        d["created_on"] = self.created_on
        d["order_id"] = self.order_id
        d["associated_on"] = self.associated_on
        return d

    def __repr__(self):
        return "QR Code url: %s"%(self.url)

class Order(db.Model):
    __tablename__ = "orders"
    id                          =db.Column      (db.Integer, primary_key = True)
    order_id                    =db.Column      (db.String(250), unique = True, index = True)
    customer_name               =db.Column      (db.String(250))
    phone_number                =db.Column      (db.String(250))
    product_name                =db.Column      (db.String(250))
    address                     =db.Column      (db.Text)

    def __repr__(self):
        return "Order_id: %s"%(self.order_id)

    def serialize(self):
        d = {}
        d["order_id"] = self.order_id
        d["customer_name"] = self.customer_name
        d["phone_number"] = self.phone_number
        d["address"] = self.address
        return d
