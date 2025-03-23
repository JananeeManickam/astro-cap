import requests
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# NASA API Key
NASA_API_KEY = "4mfkUeKtrdZBUqzX93T2Ez9IaQWRHtdL82LnitIT"
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

@csrf_exempt
def asteroid_list(request):
    """Fetch and display Near-Earth Objects (NEOs) for a given date range."""

    # Get today's date as default if no date is provided
    today = datetime.date.today()
    start_date = request.GET.get("start_date", today.strftime("%Y-%m-%d"))
    end_date = request.GET.get("end_date", start_date)  # Default to the same day if no end date

    # Construct API URL
    api_url = f"{BASE_URL}?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}"
    response = requests.get(api_url)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch asteroid data.", "details": response.json()}, status=response.status_code)

    data = response.json()
    near_earth_objects = data.get("near_earth_objects", {})

    asteroids = []
    
    # Iterate through each date and extract asteroid details
    for date, objects in near_earth_objects.items():
        for obj in objects:
            close_approach = obj["close_approach_data"][0]  # Get the first close approach
            asteroids.append({
                "id": obj["id"],
                "name": obj["name"],
                "nasa_jpl_url": obj["nasa_jpl_url"],
                "absolute_magnitude_h": obj["absolute_magnitude_h"],
                "estimated_diameter_km": {
                    "min": obj["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                    "max": obj["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                },
                "is_potentially_hazardous": obj["is_potentially_hazardous_asteroid"],
                "close_approach_date": close_approach["close_approach_date"],
                "relative_velocity_kph": close_approach["relative_velocity"]["kilometers_per_hour"],
                "miss_distance_km": close_approach["miss_distance"]["kilometers"],
                "orbiting_body": close_approach["orbiting_body"]
            })

    # Render the template with asteroid data
    return render(request, "asteroids_list.html", {"asteroids": asteroids, "start_date": start_date, "end_date": end_date})
