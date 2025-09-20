from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple Nigerian foods + calories lookup table
FOOD_DB = {
    "rice": 130,         # per 100g
    "beans": 140,
    "eba": 350,
    "fufu": 330,
    "yam": 118,
    "plantain": 122,
    "egusi soup": 250,
    "jollof rice": 200,
    "akara": 150,
}

@app.route("/parse", methods=["POST"])
def parse_food_log():
    data = request.get_json()
    food_log = data.get("food_log", "")

    if not food_log.strip():
        return jsonify({"error": "Food log is empty."}), 400

    # Naive parser: check for food names in text
    found_items = []
    total_calories = 0
    for food, cal in FOOD_DB.items():
        if food in food_log.lower():
            found_items.append({"food": food, "calories": cal})
            total_calories += cal

    return jsonify({
        "parsed_items": found_items,
        "total_calories": total_calories
    })
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
