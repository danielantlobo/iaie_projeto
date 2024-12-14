from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for products
products = [
    {"id": 1, "name": "Product A", "quantity": 50},
    {"id": 2, "name": "Product B", "quantity": 30},
    {"id": 3, "name": "Product C", "quantity": 20},
]

# Helper function to generate a new product ID
def generate_product_id():
    if products:
        return max(product['id'] for product in products) + 1
    return 1

# Route to render the supplier dashboard
@app.route('/')
def supplier_dashboard():
    return render_template('index_supplier.html', products=products)

# API route to add a new product
@app.route('/api/products', methods=['POST'])
def add_product():
    try:
        # Get the form data
        name = request.form['name']
        quantity = int(request.form['quantity'])

        # Validate inputs
        if not name or quantity < 0:
            return jsonify({"error": "Invalid product data"}), 400

        # Create a new product
        new_product = {
            "id": generate_product_id(),
            "name": name,
            "quantity": quantity
        }
        products.append(new_product)

        return jsonify({"message": "Product added successfully", "product": new_product}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
