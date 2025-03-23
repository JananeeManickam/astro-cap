import requests
import logging

logging.basicConfig(level=logging.INFO)

from django.http import HttpResponse

def telescope_live_view(telescope_name):
    """
    Render the telescope's live observation page in an iframe.
    """
    print("inside...")

    url = "https://api.jwstapi.com/program/list?"

    payload={}
    headers = {
    'X-API-KEY': '0edf3656-7555-42bd-9d10-da951016f4d7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    # print("name:",telescope_name)
    # url = f"https://spacetelescopelive.org/{telescope_name}/"
    # # response = requests.get(url)
    # # print("Response Content:\n", response.text[:500])
    # print(f"{url}")
    # html_content = f"""
    # <html>
    # <head>
    #     <title>{telescope_name.capitalize()} Live View</title>
    #     <meta http-equiv="refresh" content="30"> <!-- Auto-refresh every 30 seconds -->
    #     <style>
    #         body {{ margin: 0; padding: 0; text-align: center; }}
    #         iframe {{ width: 100vw; height: 100vh; border: none; }}
    #     </style>
    # </head>
    # <body>
    #     <iframe src="{url}" allowfullscreen></iframe>
    # </body>
    # </html>
    # """
    # # html_content = f"""{response}"""
    # return HttpResponse(html_content)
