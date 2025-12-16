from django.core.management.base import BaseCommand
from api.models import Food

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

class Command(BaseCommand):
    help = "Load Nigerian foods into database"

    def handle(self, *args, **kwargs):
        for name, data in CALORIE_DATABASE.items():
            Food.objects.get_or_create(
                name=name,
                defaults={"calories_per_100g": data["calories_per_100g"], "unit": data["unit"]}
            )
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {Food.objects.count()} foods into the database.")
        )