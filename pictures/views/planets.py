# import json
# import os
# import datetime
# import requests
# from django.shortcuts import render
# from django.views import View
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# PLANET_API_KEY = 'PLAK8795c46a13dd45589728b698fb8b20f3'
# BASE_URL = 'https://api.planet.com/data/v1'

# # Available planets
# AVAILABLE_PLANETS = ["mars", "neptune"]

# class PlanetListView(View):
#     """Dynamically fetch available planets."""
    
#     def get(self, request):
#         return render(request, 'planets_list.html', {"planets": AVAILABLE_PLANETS})


# @csrf_exempt
# def get_planet_photo(request, planet_name):
#     """Fetch planetary image data from Planet API dynamically."""

#     if request.method != "GET":
#         return JsonResponse({"error": "Only GET requests are allowed."}, status=405)

#     if not PLANET_API_KEY:
#         return JsonResponse({"error": "Planet API key not set."}, status=500)

#     # Convert date to Unix timestamp
#     date_string = "2024-01-01T00:00:00Z"
#     date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
#     timestamp = int(date_obj.timestamp())  # Convert to Unix timestamp

#     # Set up session with authentication
#     session = requests.Session()
#     session.auth = (PLANET_API_KEY, "")

#     # Construct API request URL for searching images
#     search_url = f"{BASE_URL}/quick-search"

#     # Define the search query with valid filtering fields
#     query = {
#         "item_types": ["PSScene"],  # ✅ Valid item type
#         "filter": {
#             "type": "DateRangeFilter",
#             "field_name": "acquired",  # ✅ Correct field name for timestamp
#             "config": {
#                 "gte": "2024-01-01T00:00:00Z",  # ✅ Correct format
#                 "lte": "2024-03-01T00:00:00Z"   # Optional: limit date range
#             }
#         }
#     }


#     # Send the search request
#     response = session.post(search_url, json=query)
#     print(response.status_code)  # Debugging
#     print(response.text)
    


#     if response.status_code == 200:
#         data = response.json()
#         features = data.get("features", [])

#         if not features:
#             return JsonResponse({"message": f"No images found for {planet_name}."}, safe=False)

#         # Extract first image
#         image_info = features[0]
#         image_id = image_info.get("id")

#         # Retrieve asset information
#         assets_url = f"{BASE_URL}/items/{image_id}/assets/"
#         assets_response = session.get(assets_url)

#         if assets_response.status_code == 200:
#             assets = assets_response.json()
#             visual_asset = assets.get('visual')

#             if visual_asset:
#                 # Activate the asset if not already active
#                 if visual_asset.get('status') != 'active':
#                     activation_url = visual_asset['_links']['activate']
#                     activation_response = session.post(activation_url)
#                     if activation_response.status_code not in [200, 202]:
#                         return JsonResponse({"error": "Failed to activate the image asset."}, status=activation_response.status_code)

#                 # Return image details
#                 return JsonResponse({
#                     "planet": planet_name.capitalize(),
#                     "image_id": image_id,
#                     "image_url": visual_asset['location'],
#                     "metadata": image_info.get("properties", {})
#                 })
#             else:
#                 return JsonResponse({"error": "No visual asset found for the selected image."}, safe=False)
#         else:
#             return JsonResponse({"error": "Failed to retrieve asset information."}, status=assets_response.status_code)

#     else:
#         return JsonResponse({
#             "error": f"Failed to fetch {planet_name} data from Planet API.",
#             "response": response.json()  # Include API error message
#         }, status=response.status_code)

from django.shortcuts import render
from django.views import View
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# NASA API Key
PLANET_API_KEY = '4mfkUeKtrdZBUqzX93T2Ez9IaQWRHtdL82LnitIT'
BASE_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
AVAILABLE_PLANETS = ["mars", "neptune"]

class PlanetListView(View):
    """Dynamically fetch available planets."""
    
    def get(self, request):
        return render(request, 'planets_list.html', {"planets": AVAILABLE_PLANETS})



@csrf_exempt
def get_planet_photo(request, planet_name):
    """Fetch Mars images from NASA's API."""
    
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed."}, status=405)

    if planet_name.lower() != "mars":
        return JsonResponse({"error": "Only Mars images are supported."}, status=400)

    # Fetch images from Mars rover using a specific sol (Martian day)
    sol = 1000  # Example sol, can be parameterized
    api_url = f"{BASE_URL}?sol={sol}&api_key={PLANET_API_KEY}"

    response = requests.get(api_url)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch Mars images.", "details": response.json()}, status=response.status_code)

    data = response.json()
    photos = data.get("photos", [])

    if not photos:
        return JsonResponse({"message": "No images found for the given sol."}, safe=False)

    # Extract relevant image details
    images = []
    for photo in photos[:10]:  # Limit to first 10 images
        images.append({
            "id": photo["id"],
            "img_src": photo["img_src"],
            "earth_date": photo["earth_date"],
            "camera": {
                "name": photo["camera"]["name"],
                "full_name": photo["camera"]["full_name"]
            },
            "rover": {
                "name": photo["rover"]["name"],
                "landing_date": photo["rover"]["landing_date"],
                "status": photo["rover"]["status"]
            }
        })

    return JsonResponse({"planet": "Mars", "images": images}, safe=False)
