#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


# GET /bakeries
@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    response = make_response(
        jsonify([bakery.to_dict() for bakery in all_bakeries]),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


# GET /bakeries/<int:id>
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    response = make_response(
        jsonify(bakery.to_dict(rules=('-baked_goods.bakery',))),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


# GET /baked_goods/by_price
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = make_response(
        jsonify([bg.to_dict(rules=('-bakery.baked_goods',)) for bg in goods]),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


# GET /baked_goods/most_expensive
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        response = make_response(
            jsonify(baked_good.to_dict(rules=('-bakery.baked_goods',))),
            200
        )
    else:
        response = make_response(
            jsonify({'error': 'No baked goods found'}),
            404
        )
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
