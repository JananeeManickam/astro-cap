from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class StellariumSkyView(APIView):
    """
    View to redirect to the Stellarium web app.
    """
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny] 
    def get(self, request):
        """
        Handle GET requests to redirect to the Stellarium web application.
        """
        print("in 1")
        # URL for the Stellarium web app
        stellarium_web_url = 'https://stellarium-web.org/'  # Update this URL as necessary
        
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stellarium Web Access</title>
        </head>
        <body>
            <h3>Click the button below to open Stellarium Web:</h3>
            <button onclick="window.open('{stellarium_web_url}', '_blank')">Launch Stellarium Web</button>
        </body>
        </html>
        """
        
        return HttpResponse(html_response)


# import requests
# import subprocess
# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class StellariumSkyView(APIView):
#     """
#     View to interact with the Stellarium API to get sky data and launch Stellarium.
#     """

#     def get(self, request):
#         """
#         Handle GET requests to retrieve sky data from Stellarium and launch the application.
#         """
#         # Path to the Stellarium executable
#         stellarium_path = "C:\\Program Files\\Stellarium\\stellarium.exe"  # Update this path as necessary

#         # Launch Stellarium
#         try:
#             subprocess.Popen([stellarium_path])
#         except Exception as e:
#             return Response({'error': f'Failed to launch Stellarium: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # URL for the Stellarium API
#         url = 'http://localhost:8090/api/sky'  # Stellarium API endpoint

#         try:
#             print("trying")
#             # Send a GET request to the Stellarium API
#             response = requests.get(url)

#             # Check if the response was successful
#             response.raise_for_status() 
#             print(response)

#             # Return the JSON response from Stellarium
#             return Response(response.json(), status=status.HTTP_200_OK)

#         except requests.exceptions.HTTPError as http_err:
#             # Handle HTTP errors (e.g., 400, 404, 500)
#             return Response({'error': str(http_err)}, status=response.status_code)

#         except requests.exceptions.RequestException as req_err:
#             # Handle other request exceptions (e.g., connection errors)
#             return Response({'error': str(req_err)}, status=status.HTTP_400_BAD_REQUEST)