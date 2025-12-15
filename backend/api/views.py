from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .utils import parse_food_log

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["POST"])
def parse_log(request):
    """
    Handles POST requests to the /parse-log endpoint.
    Expects a JSON payload with a 'foodLog' key.
    """
    try:
        data = json.loads(request.body)
        if not data or 'foodLog' not in data:
            return JsonResponse({"error": "Invalid request. 'foodLog' key is missing."}, status=400)

        food_log = data['foodLog']

        # Call the logic function
        parsed_items, total_calories = parse_food_log(food_log)

        logger.info(f"Received food log: {food_log[:50]}...")
        logger.info(f"Parsed items: {parsed_items}")
        logger.info(f"Total calories: {total_calories}")

        return JsonResponse({
            "status": "success",
            "message": "Food log processed and calories calculated.",
            "parsed_items": parsed_items,
            "total_calories": total_calories
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
