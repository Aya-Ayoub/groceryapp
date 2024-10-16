from flask import Flask, request, jsonify, Blueprint
from authentication import authenticate_token

grocery_bp = Blueprint("grocery", __name__)

products = []

@grocery_bp.before_request
def before_request():
    authenticate_token()

#new product
@grocery_bp.route("/", methods=["POST"])
def create_product():
    product = {
        "id": len(products) + 1,
        "name": request.json.get("name"),
        "price": request.json.get("price"),
        "quantity": request.json.get("quantity"),
    }
    products.append(product)
    return jsonify(product), 201

#Get all products
@grocery_bp.route("/", methods=["GET"])
def get_products():
    return jsonify(products)

#Get product by ID
@grocery_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

#Update product by ID
@grocery_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    product["name"] = request.json.get("name", product["name"])
    product["price"] = request.json.get("price", product["price"])
    product["quantity"] = request.json.get("quantity", product["quantity"])
    return jsonify(product)

#Delete product by ID
@grocery_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    global products
    products = [p for p in products if p["id"] != id]
    return '', 204
