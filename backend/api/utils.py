import re
from fractions import Fraction

# Calorie values are rough estimates for demonstration purposes only.
CALORIE_DATABASE = {
    # Swallows & Staples
    'eba': {'calories_per_100g': 381, 'unit': 'g'},
    'fufu': {'calories_per_100g': 180, 'unit': 'g'},
    'amala': {'calories_per_100g': 250, 'unit': 'g'},
    'pounded yam': {'calories_per_100g': 235, 'unit': 'g'},
    'semovita': {'calories_per_100g': 107, 'unit': 'g'},
    'lafun': {'calories_per_100g': 357, 'unit': 'g'},
    'yam flour': {'calories_per_100g': 356, 'unit': 'g'},
    'plantain flour': {'calories_per_100g': 350, 'unit': 'g'},
    'cassava flour': {'calories_per_100g': 160, 'unit': 'g'},
    'wheat flour': {'calories_per_100g': 455, 'unit': 'g'},
    'oat flour': {'calories_per_100g': 404, 'unit': 'g'},
    'semolina': {'calories_per_100g': 360, 'unit': 'g'},
    'fonio': {'calories_per_100g': 360, 'unit': 'g'},
    'sorghum': {'calories_per_100g': 329, 'unit': 'g'},
    'millet': {'calories_per_100g': 378, 'unit': 'g'},
    'maize': {'calories_per_100g': 365, 'unit': 'g'},
    'maize flour': {'calories_per_100g': 365, 'unit': 'g'},
    'barley': {'calories_per_100g': 354, 'unit': 'g'},
    'teff': {'calories_per_100g': 367, 'unit': 'g'},
    'quinoa': {'calories_per_100g': 368, 'unit': 'g'},
    'rice flour': {'calories_per_100g': 366, 'unit': 'g'},
    'ofada rice': {'calories_per_100g': 360, 'unit': 'g'},
    'white rice': {'calories_per_100g': 130, 'unit': 'g'},
    'brown rice': {'calories_per_100g': 112, 'unit': 'g'},
    'basmati rice': {'calories_per_100g': 121, 'unit': 'g'},
    # Dishes
    'jollof rice': {'calories_per_100g': 130, 'unit': 'g'},
    'fried rice': {'calories_per_100g': 150, 'unit': 'g'},
    'moi moi': {'calories_per_100g': 200, 'unit': 'g'},
    'okpa': {'calories_per_100g': 216, 'unit': 'g'},
    'abacha': {'calories_per_100g': 367, 'unit': 'g'},
    'egusi soup': {'calories_per_100g': 593, 'unit': 'g'},
    'banga soup': {'calories_per_100g': 440, 'unit': 'g'},
    'ogbono soup': {'calories_per_100g': 400, 'unit': 'g'},
    'afang soup': {'calories_per_100g': 350, 'unit': 'g'},
    'efo riro': {'calories_per_100g': 300, 'unit': 'g'},
    'nsala soup': {'calories_per_100g': 450, 'unit': 'g'},
    'oha soup': {'calories_per_100g': 400, 'unit': 'g'},
    'okro soup': {'calories_per_100g': 250, 'unit': 'g'},
    'gbegiri soup': {'calories_per_100g': 200, 'unit': 'g'},
    'ewedu soup': {'calories_per_100g': 97, 'unit': 'g'},
    # Proteins & Meats
    'goat meat': {'calories_per_100g': 143, 'unit': 'g'},
    'beef': {'calories_per_100g': 250, 'unit': 'g'},
    'chicken': {'calories_per_100g': 239, 'unit': 'g'},
    'turkey': {'calories_per_100g': 135, 'unit': 'g'},
    'snail': {'calories_per_100g': 90, 'unit': 'g'},
    'fish': {'calories_per_100g': 128, 'unit': 'g'},
    'crayfish': {'calories_per_100g': 280, 'unit': 'g'},
    'stockfish': {'calories_per_100g': 200, 'unit': 'g'},
    'suya': {'calories_per_100g': 250, 'unit': 'g'},
    'isi ewu': {'calories_per_100g': 300, 'unit': 'g'},
    # Snacks & Sides
    'kuli kuli': {'calories_per_100g': 500, 'unit': 'g'},
    # Breads
    'white bread': {'calories_per_100g': 266, 'unit': 'g'},
    'whole wheat bread': {'calories_per_100g': 260, 'unit': 'g'},
    'banana bread': {'calories_per_100g': 326, 'unit': 'g'},
    'almond bread': {'calories_per_100g': 313, 'unit': 'g'},
    # Beans
    'beans': {'calories_per_100g': 127, 'unit': 'g'},
    'ewa aganyin': {'calories_per_100g': 520, 'unit': 'g'},
    # Oils & Nuts
    'groundnut oil': {'calories_per_100g': 884, 'unit': 'g'},
    'palm oil': {'calories_per_100g': 884, 'unit': 'g'},
    'groundnut': {'calories_per_100g': 567, 'unit': 'g'},
    'cashew nuts': {'calories_per_100g': 553, 'unit': 'g'},
    'almonds': {'calories_per_100g': 579, 'unit': 'g'},
    'walnuts': {'calories_per_100g': 654, 'unit': 'g'},
    'coconut': {'calories_per_100g': 660, 'unit': 'g'},
    # Tubers & Roots
    'yam': {'calories_per_100g': 116, 'unit': 'g'},
    'sweet potato': {'calories_per_100g': 86, 'unit': 'g'},
    'irish potato': {'calories_per_100g': 77, 'unit': 'g'},
    'cassava': {'calories_per_100g': 160, 'unit': 'g'},
    'coco yam': {'calories_per_100g': 168, 'unit': 'g'},
    # Fruits & Vegetables (examples)
    'banana': {'calories_per_100g': 89, 'unit': 'g'},
    'orange': {'calories_per_100g': 47, 'unit': 'g'},
    'pineapple': {'calories_per_100g': 50, 'unit': 'g'},
    'pawpaw': {'calories_per_100g': 43, 'unit': 'g'},
    'mango': {'calories_per_100g': 60, 'unit': 'g'},
    'carrot': {'calories_per_100g': 41, 'unit': 'g'},
    'cucumber': {'calories_per_100g': 16, 'unit': 'g'},
    'lettuce': {'calories_per_100g': 15, 'unit': 'g'},
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
    'plate': 250,
    'bowl': 350,
    'derica': 450,  # Approximate grams in a derica cup
    'g': 1,
    'gram': 1,
    'grams': 1,
    'ml': 1,
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
                calories_per_unit = CALORIE_DATABASE[food_item]['calories_per_100g']

                # Final calculation.
                calories = calories_per_unit * quantity * unit_factor
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
                total_calories += calories_today
                
                parsed_items.append({
                    "item": food_item,
                    "quantity": f"{quantity} {food_item_str}",
                    "total_calories": round(calories, 2),
                    "calories_today": round(calories_today, 2),
                })
    
    return parsed_items, round(total_calories, 2)
