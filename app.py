from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Hat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)
    image = db.Column(db.String, nullable = False)

    def __init__(self, type, price, image):
        self.type = type 
        self.price = price
        self.image = image

class HatSchema(ma.Schema):
    class Meta:
        fields = ("id", "type", "price", "image")

hat_schema = HatSchema()
hats_schema = HatSchema(many = True)

@app.route("/", methods = ["GET","POST"])
def hello():
    return "Hello from Khalil's API"

@app.route("/hat/add", methods = ["POST"])
def add_hat():
    type = request.json.get("type")
    price = request.json.get("price")
    image = request.json.get("image")

    record = Hat(type, price, image)
    db.session.add(record)
    db.session.commit()

    return jsonify(hat_schema.dump(record))

@app.route("/hat/get", methods = ["GET"])
def get_hat():
    all_hats = Hat.query.all()
    return jsonify(hats_schema.dump(all_hats))

@app.route("/hat/<id>", methods=["DELETE"])
def delete(id):
    hat = Hat.query.get(id)
    db.session.delete(hat)
    db.session.commit()
    return "Hat deleted"




if __name__ == "__main__":
    app.run(debug=True)



