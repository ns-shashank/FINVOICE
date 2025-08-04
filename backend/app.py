from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend without CORS issues

# In-memory storage (consider using a database later)
expenses = []

@app.route("/")
def index():
    return jsonify({"message": "Welcome to FinVoice backend"}), 200

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.get_json()

    if not data or "amount" not in data or "category" not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        amount = float(data["amount"])
        category = data["category"]
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a number"}), 400

    expenses.append({"amount": amount, "category": category})
    return jsonify({"message": "Expense added successfully"}), 200

@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses), 200

@app.route("/clear_expenses", methods=["POST"])
def clear_expenses():
    expenses.clear()
    return jsonify({"message": "All expenses cleared"}), 200

if __name__ == "__main__":
    app.run(debug=True)
