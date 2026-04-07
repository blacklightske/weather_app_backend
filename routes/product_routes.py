from flask import Blueprint
from views.product_views import (
    home,
    get_products,
    add_products,
    update_product,
    partial_update_product,
    delete_product,
    get_product_by_id,
    add_category
)

product_bp = Blueprint("product_bp", __name__)

product_bp.route("/", methods=["GET"])(home)
product_bp.route("/products", methods=["GET"])(get_products)
product_bp.route("/products", methods=["POST"])(add_products)
product_bp.route("/products/<int:id>", methods=["PUT"])(update_product)
product_bp.route("/products/<int:id>", methods=["PATCH"])(partial_update_product)
product_bp.route("/products/<int:id>", methods=["DELETE"])(delete_product)
product_bp.route("/products/<int:id>", methods=["GET"])(get_product_by_id)
product_bp.route("/products/<int:id>", methods=["POST"])(add_category)

