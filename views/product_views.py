from flask import jsonify, request
from models.product import Product
from db.database import db
from models.category import Category
from sqlalchemy.exc import IntegrityError


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
    category_id = data.get("category_id")

    if name is None or price is None:
        return jsonify({"message": "Missing fields"}), 400
    if not isinstance(name, str) or not name.strip():#isinstance checks,,, is this value of this type?
        return jsonify({"message": "Name must be a non-empty string"}), 400

    if not isinstance(price, (int, float)):
        return jsonify({"message": "Price must be a number"}), 400

    if price < 0:
        return jsonify({"message": "Price cannot be negative"}), 400
    if category_id is None:
        return jsonify({"message": "category_id is required"}), 400

    product = Product()
    product.name = name
    product.price = price
    product.description = description
    product.category_id = category_id

    try:
        db.session.add(product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "message": "Product with this name already exists in this category"
        }), 400
    
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
    if not isinstance(name, str) or not name.strip():
        return jsonify({"message": "Name must be a non-empty string"}), 400

    if not isinstance(price, (int, float)):
        return jsonify({"message": "Price must be a number"}), 400

    if price < 0:
        return jsonify({"message": "Price cannot be negative"}), 400

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

def get_categories():
    from models.category import Category

    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200    

def add_category():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 415

    data = request.get_json()

    name = data.get("name")

    if name is None or not isinstance(name, str) or not name.strip():
        return jsonify({"message": "Name must be a non-empty string"}), 400

    

    category = Category()
    category.name = name.strip()
    
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Category already exists"}), 400

    return jsonify({
        "message": "Category created successfully",
        "category": category.to_dict()
    }), 201


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
        if not isinstance(name, str) or not name.strip():
            return jsonify({"message": "Name must be a non-empty string"}), 400
        product.name = name.strip()

    if price is not None:
        if not isinstance(price, (int, float)):
            return jsonify({"message": "Price must be a number"}), 400
        if price < 0:
            return jsonify({"message": "Price cannot be negative"}), 400
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