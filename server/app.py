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

@app.route('/bakeries')
def get_all_bakeries():
    bakeries =Bakery.query.all()
    bakery_list = [b.to_dict() for b in bakeries]
    return make_response(bakery_list, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    return make_response({"error": "Bakery not found"}, 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [g.to_dict() for g in goods]
    return make_response(goods_list, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return make_response(most_expensive.to_dict(), 200)
    return make_response({"error": "No baked goods found"}, 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
