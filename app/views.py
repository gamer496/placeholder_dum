from flask import jsonify, request
from app import app, db
from models import QrCode, Order
import cloudinary.uploader
import qrcode
import uuid
import ipdb

@app.errorhandler(404)
def page_not_found(e = ""):
    return jsonify({"err": "404 error page not found bitch"}), 404

@app.errorhandler(403)
def not_authorized(e = ""):
    return jsonify({"err": "403 not authorized. Sorry but you are not authorized to perform operations on this content"}), 403

@app.errorhandler(400)
def something_missing(e = ""):
    return jsonify({"err": "Arguments provided were not enough to carry out this request"}), 400

@app.errorhandler(500)
def internal_error(e = ""):
    return jsonify({"err": "Hmm looks like our servers are not working the way they should be. Kindly try again after sometime"}), 500

def as_msg(s, errors = []):
    return jsonify({"err": "there seems to be some error", "description": s, "errors": []})


@app.route("/index", methods = ["GET", "POST"])
def index():
    return jsonify({"msg": "hello world"})

@app.route("/qr", methods = ["GET"])
def generate_qr_code():
    uid = str(uuid.uuid4())
    qr = qrcode.make(uid)
    qr.save("tmp.png")
    d = cloudinary.uploader.upload("tmp.png")
    try:
        public_id, version, image_format, url, secure_url = d["public_id"], d["version"], d["format"], d["url"], d["secure_url"]
        qr_obj = QrCode()
        qr_obj.public_id = public_id
        qr_obj.url = secure_url
        qr_obj.uid = uid
        db.session.add(qr_obj)
        db.session.commit()
    except:
        print "cloudinary seems to down"
        return page_not_found()
    return jsonify({"public_id": qr_obj.public_id, "secure_url": qr_obj.url})

@app.route("/associate", methods = ["POST"])
def associate():
    try:
        data = request.json
    except:
        print "no json in request"
        return something_missing()
    try:
        qr_code = QrCode.query.filter(QrCode.uid == data["uuid"])[0]
    except:
        return as_msg("no such qr code present")
    try:
        order_id = data["order_id"]
        address = data["address"]
        customer_name = data["customer_name"]
        product_name = data["product_name"]
        phone_no = data["phone_number"]
    except:
        return something_missing()
    order = Order()
    order.address = address
    order.customer_name = customer_name
    order.product_name = product_name
    order.phone_number = phone_number
    order.order_id = order_id
    qr_code.order_id = order_id
    qr_code.set_associated_on()
    db.session.add(order)
    db.session.add(qr_code)
    db.session.commit()
    return jsonify({"msg": "successfully associated"})

@app.route("/getorderdetails", methods = ["GET"])
def get_order_details():
    try:
        uuid = request.args.get('uuid')
        qr = QrCode.query.filter(QrCode.uid == uuid)[0]
        order = Order.query.filter(Order.order_id == qr.order_id)[0]
    except:
        return as_msg("no order_id to this qr code")
    return jsonify(order.serialize())

@app.route("/getqrcodeinfo", methods = ["GET"])
def get_qr_code_info():
    try:
        uuid = request.args.get('uuid')
        qr = QrCode.query.filter(QrCode.uid == uuid)[0]
        return jsonify(qr.serialize())
    except:
        return as_msg("no qr code associated with this uuid")
