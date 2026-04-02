from flask import jsonify, request
from models.product import Product
from db.database import db


def home():
    return jsonify({"message": "hello from our first flask server"})


def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


def add_products():
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400

    product = Product(name=name, price=price)

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "product added safely",
        "product": product.to_dict()
    }), 201


def update_product(id):
    return jsonify({"message": "PUT not converted to ORM yet"}), 501


def partial_update_product(id):
    return jsonify({"message": "PATCH not converted to ORM yet"}), 501


def delete_product(id):
    return jsonify({"message": "DELETE not converted to ORM yet"}), 501