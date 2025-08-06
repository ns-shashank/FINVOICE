from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)
expenses = []

def parse_expense(text):
    # Extract amount and item from voice
    amount_match = re.search(r"(\d+)", text)
    if not amount_match:
        return None

    amount = int(amount_match.group(1))
    item = text.replace(str(amount), "").replace("rupees", "").strip()

    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "amount": amount,
        "item": item
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    transcript = data.get("transcript", "").lower()

    if "show expenses" in transcript:
        return jsonify({"expenses": expenses})

    if "done" in transcript:
        return jsonify({"message": "done"})

    expense = parse_expense(transcript)
    if expense:
        expenses.append(expense)
        return jsonify({"message": "Expense recorded"})
    else:
        return jsonify({"message": "Could not parse expense"})

if __name__ == "__main__":
    app.run(debug=True)
