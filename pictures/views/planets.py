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
