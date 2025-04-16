from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from other domains like Vercel

# Load product data from file
with open("products.json") as f:
    PRODUCTS = json.load(f)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    results = []

    for product in PRODUCTS:
        name = product.get("name", "").lower()
        sku = product.get("sku", "").lower()
        if query in name or query in sku:
            results.append(product)

    if not results:
        names = [p["name"] for p in PRODUCTS]
        close_matches = get_close_matches(query, names, n=5, cutoff=0.3)
        results = [p for p in PRODUCTS if p["name"] in close_matches]

    return jsonify(results[:10])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
