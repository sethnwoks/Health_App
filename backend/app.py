import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from fractions import Fraction

# The Flask app instance. This is our server.
app = Flask(__name__)
# Enable CORS for all routes. This lets your React app talk to the Flask server.
CORS(app)

# This is a placeholder for your food calorie database.
# In a real application, you would connect to a proper database like PostgreSQL.
# Calorie values are rough estimates for demonstration purposes only.
CALORIE_DATABASE = {
    'eba': {'calories_per_100g': 360, 'unit': 'g'},
    'egusi soup': {'calories_per_100ml': 150, 'unit': 'ml'},
    'rice': {'calories_per_100g': 130, 'unit': 'g'},
    'yam': {'calories_per_100g': 160, 'unit': 'g'},
    'stew': {'calories_per_100ml': 120, 'unit': 'ml'},
}

# A simple "database" for text-to-number conversion.
NUMBER_WORDS = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
}

# A simple "database" for unit conversion (in ml for liquid, g for solid).
UNITS = {
    'gallon': 3785.41,
    'cup': 240,
    'plate': 250, # Rough estimate in g for a plate of solid food
    'bowl': 350,  # Rough estimate in g for a bowl of solid food
}

def parse_food_log(log_text):
    """
    Parses a food log using a more advanced rule-based NLP approach.
    This function handles quantities, fractions, units, and food items.
    It returns a list of dictionaries with parsed data.
    """
    # Normalize the text to lower case to make matching easier.
    log_text = log_text.lower()
    
    parsed_items = []
    total_calories = 0

    # Split the log into separate entries based on newlines or common separators.
    entries = re.split(r'\n|,| and ', log_text)

    for entry in entries:
        # A simple check to find quantities and their food items.
        # This regex is a bit smarter now to handle more cases.
        match = re.search(r'(\d+(?:\s?[-/]\s?\d+)?|' + '|'.join(NUMBER_WORDS.keys()) + r')\s+([a-zA-Z\s]+)', entry)
        
        if match:
            # Get the quantity and the raw food item string.
            quantity_str, food_item_str = match.groups()

            # Convert the quantity string to a number.
            quantity = 0
            if '/' in quantity_str:
                quantity = float(Fraction(quantity_str))
            elif '-' in quantity_str:
                # Handle "1-3rd" by just getting the fraction. This is a simplification.
                parts = quantity_str.split('-')
                if parts[1] == '3rd':
                    quantity = 1/3
            elif quantity_str in NUMBER_WORDS:
                quantity = NUMBER_WORDS[quantity_str]
            else:
                try:
                    quantity = float(quantity_str)
                except (ValueError, TypeError):
                    continue # Skip if we can't parse the number.

            # Find the best match for the food item in our database.
            # This is a simple fuzzy match; we check for the longest matching item first.
            food_item = None
            for item in sorted(CALORIE_DATABASE.keys(), key=len, reverse=True):
                if item in food_item_str:
                    food_item = item
                    break

            if food_item:
                # Find the unit and calculate the calorie value.
                unit_factor = 1.0
                for unit_word, factor in UNITS.items():
                    if unit_word in food_item_str:
                        unit_factor = factor / 100 # Assuming base is per 100g/ml
                        break

                # Get the calories from our database.
                calories_per_unit = list(CALORIE_DATABASE[food_item].values())[0]

                # Final calculation.
                calories = calories_per_unit * quantity * unit_factor
                total_calories += calories

                # Check if the user mentioned a fraction of what they ate today.
                daily_fraction = 1.0
                if 'today' in entry:
                    # A very simple rule: if "today" is mentioned, look for a fraction.
                    fraction_match = re.search(r'(\d+/\d+|one-third|one third|one half)', entry)
                    if fraction_match:
                        fraction_str = fraction_match.group(1)
                        if 'third' in fraction_str:
                            daily_fraction = 1/3
                        elif 'half' in fraction_str or '1/2' in fraction_str:
                            daily_fraction = 0.5
                        else:
                            try:
                                daily_fraction = float(Fraction(fraction_str))
                            except ValueError:
                                pass # Use the default 1.0 if we can't parse it.

                calories_today = calories * daily_fraction
                
                parsed_items.append({
                    "item": food_item,
                    "quantity": f"{quantity} {food_item_str}",
                    "total_calories": round(calories, 2),
                    "calories_today": round(calories_today, 2),
                })
    
    return parsed_items, round(total_calories, 2)

# The API endpoint for parsing the food log.
@app.route('/parse-log', methods=['POST'])
def parse_log():
    """
    Handles POST requests to the /parse-log endpoint.
    Expects a JSON payload with a 'foodLog' key.
    """
    try:
        data = request.get_json()
        if not data or 'foodLog' not in data:
            return jsonify({"error": "Invalid request. 'foodLog' key is missing."}), 400

        food_log = data['foodLog']

        # Call the new, more powerful calorie calculation function.
        parsed_items, total_calories = parse_food_log(food_log)

        print(f"Received food log: {food_log[:50]}...")
        print(f"Parsed items: {parsed_items}")
        print(f"Total calories: {total_calories}")

        return jsonify({
            "status": "success",
            "message": "Food log processed and calories calculated.",
            "parsed_items": parsed_items,
            "total_calories": total_calories
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# This is the standard entry point for running the Flask app.
# It ensures the server only runs when you execute this script directly.
if __name__ == '__main__':
    # 'debug=True' is for development only. NEVER use this in production.
    app.run(debug=True)
