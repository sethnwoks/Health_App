import os
from google import genai
from google.genai import types
from api.models import Food
from dotenv import load_dotenv

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


load_dotenv()

# ... (CALORIE_DATABASE and UNITS remain the same, I will reference them) ...

def lookup_food_calories(food_name: str, quantity: float, unit: str = None) -> dict:
    """
    Calculates calories for a specific food item by querying the database.
    
    Args:
        food_name: The name of the food (e.g., 'eba', 'rice').
        quantity: The amount eaten.
        unit: The unit of measurement (e.g., 'cup', 'gram', 'plate').
    
    Returns:
        Dictionary with calorie details or error.
    """
    # Normalize input
    food_name = food_name.lower().strip()
    
    # Try exact match first
    try:
        food = Food.objects.get(name=food_name)
    except Food.DoesNotExist:
        # Fall back to fuzzy match (partial matching)
        food = Food.objects.filter(name__icontains=food_name).first()
    
    if not food:
        return {"error": f"Food '{food_name}' not found in database."}
        
    # Get base calories (per 100g/ml)
    calories_per_100g = food.calories_per_100g
    
    # Calculate Unit Factor
    unit_factor = 1.0 # Default to 100g if no unit
    if unit:
        unit = unit.lower().strip()
        # Check exact match first
        if unit in UNITS:
            unit_factor = UNITS[unit] / 100
        else:
            # Check partial match
            for u_key, u_val in UNITS.items():
                if u_key in unit:
                    unit_factor = u_val / 100
                    break
    
    total_calories = calories_per_100g * quantity * unit_factor
    
    return {
        "item": food.name,
        "quantity": f"{quantity} {unit if unit else 'g'}",
        "total_calories": round(total_calories, 2),
        "calories_today": round(total_calories, 2) # Assuming full portion for now, can add fraction logic later
    }

def parse_food_log(log_text):
    """
    Uses OpenAI to parse the food log and call the lookup tool.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("DEBUG: No OPENAI_API_KEY found!")
        return [], 0
        
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    # Define the tool in OpenAI format
    tools = [
        {
            "type": "function",
            "function": {
                "name": "lookup_food_calories",
                "description": "Calculates calories for a specific food item",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "food_name": {
                            "type": "string",
                            "description": "The name of the food (e.g., 'eba', 'rice')"
                        },
                        "quantity": {
                            "type": "number",
                            "description": "The amount eaten"
                        },
                        "unit": {
                            "type": "string",
                            "description": "The unit of measurement (e.g., 'cup', 'gram', 'plate')"
                        }
                    },
                    "required": ["food_name", "quantity"]
                }
            }
        }
    ]
    
    parsed_items = []
    total_calories = 0
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a nutrition assistant. Extract food items, quantities, and units from the user's text. Call the 'lookup_food_calories' function for EACH food item found."},
                {"role": "user", "content": log_text}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        print(f"DEBUG: OpenAI Response: {message.content}")
        
        # Check if there are tool calls
        if message.tool_calls:
            print(f"DEBUG: Function calls found: {len(message.tool_calls)}")
            for tool_call in message.tool_calls:
                print(f"DEBUG: Calling tool: {tool_call.function.name} with args: {tool_call.function.arguments}")
                if tool_call.function.name == 'lookup_food_calories':
                    import json
                    args = json.loads(tool_call.function.arguments)
                    result = lookup_food_calories(
                        food_name=args.get('food_name'),
                        quantity=args.get('quantity'),
                        unit=args.get('unit')
                    )
                    print(f"DEBUG: Tool Result: {result}")
                    
                    if 'error' not in result:
                        parsed_items.append(result)
                        total_calories += result['total_calories']
                        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        pass

    return parsed_items, round(total_calories, 2)
