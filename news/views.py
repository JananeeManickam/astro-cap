
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

class SpaceNewsAPIView(APIView):
    def get(self, request):
        api_key = "de59ad6200fb4e8289b7528b9e937515"
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "astronomy OR astrophysics OR cosmology OR NASA",
            "apiKey": api_key,
            "language": "en",
            "sortBy": "publishedAt"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("articles", [])
            filtered_articles = [
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "publishedAt": article["publishedAt"]
                }
                for article in data if "astronomy" in article["title"].lower() or "space" in article["title"].lower()
            ]
            return Response({"articles": filtered_articles})
        return Response({"error": "Unable to fetch news"}, status=response.status_code)
