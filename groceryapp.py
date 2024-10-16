from flask import Flask, request, jsonify
from grocery import grocery_bp

groceryapp = Flask(__name__)

#blueprint for routes
groceryapp.register_blueprint(grocery_bp, url_prefix="/grocery")

#unknown route
@groceryapp.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    groceryapp.run(port=2000)










from flask import Flask, request, jsonify

app = Flask(__name__)

app.register_blueprint(grocery_bp, url_prefix="/grocery")

TOKEN = "mytoken"

products = []

@app.before_request
def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

#new product
@app.route("/products", methods=["POST"])
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
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

#Get product by ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

#Update product by ID
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = next((p for p in products if p["id"] == id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    product["name"] = request.json.get("name", product["name"])
    product["price"] = request.json.get("price", product["price"])
    product["quantity"] = request.json.get("quantity", product["quantity"])
    return jsonify(product)

#Delete product by ID
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    global products
    products = [p for p in products if p["id"] != id]
    return '', 204

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(port=3000)