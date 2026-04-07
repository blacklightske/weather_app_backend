from flask import jsonify, request
from models.product import Product
from db.database import db


def home():
    return jsonify({"message": "hello from our first flask server"})


def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


def add_products():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 415

    data = request.get_json()

    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400

    product = Product()
    product.name = name
    product.price = price
    product.description = description

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "product added safely",
        "product": product.to_dict()
    }), 201


def get_product_by_id(id):
    product = Product.query.get(id)

    if product is None:
        return jsonify({"message": "product not in database"}), 404

    return jsonify(product.to_dict()), 200

def update_product(id):
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 415

    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400

    product = Product.query.get(id)

    if product is None:
        return jsonify({"message": "product not in database"}), 404

    product.name = name
    product.price = price

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully",
        "product": product.to_dict()
    }), 200


def partial_update_product(id):
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 415

    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    product = Product.query.get(id)

    if product is None:
        return jsonify({"message": "product not in database"}), 404

    if name is None and price is None:
        return jsonify({"message": "No fields provided"}), 400

    if name is not None:
        product.name = name

    if price is not None:
        product.price = price

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully",
        "product": product.to_dict()
    }), 200

def delete_product(id):
    product = Product.query.get(id)

    if product is None:
        return jsonify({"message": "product not in database"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "product deleted successfully"}), 200