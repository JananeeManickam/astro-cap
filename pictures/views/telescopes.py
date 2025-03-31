from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import logging
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# 🔭 Available telescopes (Add more telescopes here)
TELESCOPES = {
    "hubble": "https://spacetelescopelive.org/hubble",
    "webb": "https://spacetelescopelive.org/webb",
}

class TelescopeListView(View):
    """
    View to list all available telescopes.
    Clicking a telescope name redirects to its live data page.
    """

    def get(self, request):
        logger.info("Fetching telescope list.")
        return render(request, "telescopes.html", {"telescopes": TELESCOPES})

def sample_view(request):
    dic = {
        "name": "sambar",
        "age" : 62
    }
    return Response(data=dic, status=200)


def get_telescope_view(request, telescope_name):
    """
    Redirects users to live telescope data.
    Expected URL: `/pictures/telescopes/<telescope_name>/`
    """
    logger.info(f"Request received for telescope: {telescope_name}")

    # Validate telescope name
    telescope_url = TELESCOPES.get(telescope_name.lower())
    if not telescope_url:
        logger.error(f"Telescope '{telescope_name}' not found.")
        return JsonResponse({"error": "Telescope not found."}, status=404)

    logger.info(f"Redirecting to {telescope_name} live data: {telescope_url}")

    # Meta refresh for redirection
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url={telescope_url}">
    </head>
    <body>
        <p>Redirecting to <a href="{telescope_url}" target="_blank">{telescope_name.title()} Telescope Live</a>...</p>
    </body>
    </html>
    """
    return HttpResponse(html_response)
