import os
from google import genai
from google.genai import types
from api.models import Food
from dotenv import load_dotenv



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
