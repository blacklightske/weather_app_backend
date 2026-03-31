from flask import jsonify, request
from services.product_service import (
    get_all_products,
    create_product,
    update_product_full,
    update_product_partial,
    delete_product_by_id
)


def home():
    return jsonify({"message": "hello from our first flask server"})


def get_products():
    return jsonify(get_all_products())


def add_products():
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400

    product = create_product(name, price)

    return jsonify({
        "message": "product added safely",
        "product": product
    }), 201


def update_product(id):
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400

    updated = update_product_full(id, name, price)

    if updated is None:
        return jsonify({"message": "product not in database"}), 404

    return jsonify({
        "message": "Product updated successfully",
        "product": updated
    })


def partial_update_product(id):
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")

    result = update_product_partial(id, name, price)

    if result is None:
        return jsonify({"message": "product not in database"}), 404

    if result == "no_fields":
        return jsonify({"message": "No fields provided"}), 400

    return jsonify({"message": "Product updated successfully"})


def delete_product(id):
    deleted = delete_product_by_id(id)

    if not deleted:
        return jsonify({"message": "product not in database"}), 404

    return jsonify({"message": "product deleted successfully"})