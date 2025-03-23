import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

class SatellitesView(APIView):
    """
    View to fetch and display upcoming satellite passes, specifically tailored for ISS and other satellites.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        satellite_id = request.GET.get('s', '25544')  # Default to ISS (25544)
        display_format = request.GET.get('format', 'all')  # Options: 'all', 'ampm', 'utc'
        api_key = "CCZE9V-ZZD6JF-8TT7TL-5FVQ"
        api_url = f"https://www.n2yo.com/passes/?s={satellite_id}&apiKey={api_key}"

        try:
            # For testing, use a static sample to avoid API rate limits
            # In production, uncomment the requests.get line
            # response = requests.get(api_url)
            # if response.status_code != 200:
            #     return Response({"error": "Failed to fetch satellite passes"}, status=500)
            # html_data = response.text
            # sample_passes = self.extract_satellite_passes(html_data)

            # # Sample data to test the rendering without making API calls
            sample_passes = [
                {
                    "date": "1-Apr 20:11",
                    "start_az": "NNW 342°",
                    "max_time": "20:16",
                    "max_az": "NE 53°",
                    "elevation": "23°",
                    "end_time": "20:21",
                    "end_az": "SE 122°",
                    "magnitude": "+0.8",
                    "info": "Map and details",
                    "visibility": "marginal"
                },
                {
                    "date": "2-Apr 19:23",
                    "start_az": "NW 328°",
                    "max_time": "19:28",
                    "max_az": "NNE 42°",
                    "elevation": "31°",
                    "end_time": "19:34",
                    "end_az": "ESE 110°",
                    "magnitude": "+0.2",
                    "info": "Map and details",
                    "visibility": "good"
                },
                {
                    "date": "3-Apr 20:12",
                    "start_az": "WNW 294°",
                    "max_time": "20:18",
                    "max_az": "N 10°",
                    "elevation": "50°",
                    "end_time": "20:24",
                    "end_az": "ENE 78°",
                    "magnitude": "-0.4",
                    "info": "Map and details",
                    "visibility": "excellent"
                },
                {
                    "date": "4-Apr 19:24",
                    "start_az": "WNW 280°",
                    "max_time": "19:30",
                    "max_az": "NNW 359°",
                    "elevation": "89°",
                    "end_time": "19:36",
                    "end_az": "E 81°",
                    "magnitude": "-0.9",
                    "info": "Map and details",
                    "visibility": "excellent"
                },
                {
                    "date": "5-Apr 20:13",
                    "start_az": "W 260°",
                    "max_time": "20:19",
                    "max_az": "NNE 30°",
                    "elevation": "52°",
                    "end_time": "20:25",
                    "end_az": "E 100°",
                    "magnitude": "-0.3",
                    "info": "Map and details",
                    "visibility": "good"
                },
                {
                    "date": "6-Apr 19:25",
                    "start_az": "W 252°",
                    "max_time": "19:31",
                    "max_az": "N 8°",
                    "elevation": "23°",
                    "end_time": "19:37",
                    "end_az": "ENE 76°",
                    "magnitude": "+0.7",
                    "info": "Map and details",
                    "visibility": "marginal"
                }
            ]

            # Format times based on display_format parameter
            formatted_passes = []
            for pass_data in sample_passes:
                if display_format == 'ampm':
                    # Convert 24h format to AM/PM format
                    formatted_pass = self.convert_to_ampm(pass_data)
                elif display_format == 'utc':
                    # Convert local time to UTC
                    formatted_pass = self.convert_to_utc(pass_data)
                else:
                    # Keep original format
                    formatted_pass = pass_data
                
                formatted_passes.append(formatted_pass)

            satellite_info = {
                "name": "SPACE STATION",
                "catalog_number": "25544, 1998-067A",
                "location": "Kovilpatti",
                "coordinates": "Lat: 9.17°, Lng: 77.87°",
                "technical_info": {
                    "uplink": "437.550",
                    "downlink": "437.550",
                    "beacon": "",
                    "mode": "1200bps AFSK",
                    "call_sign": "RS0ISS",
                    "status": "Inactive"
                }
            }

            return render(request, "iss_passes.html", {
                "satellite": satellite_info,
                "passes": formatted_passes,
                "current_format": display_format
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def convert_to_ampm(self, pass_data):
        """Convert 24-hour format times to AM/PM format"""
        formatted_pass = pass_data.copy()
        
        # Extract the date part and time part
        date_parts = pass_data["date"].split()
        if len(date_parts) == 2:
            date, time = date_parts
            hour, minute = map(int, time.split(':'))
            am_pm = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            formatted_pass["date"] = f"{date} {hour}:{minute:02d} {am_pm}"
        
        # Process max_time
        if ":" in pass_data["max_time"]:
            hour, minute = map(int, pass_data["max_time"].split(':'))
            am_pm = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            formatted_pass["max_time"] = f"{hour}:{minute:02d} {am_pm}"
        
        # Process end_time
        if ":" in pass_data["end_time"]:
            hour, minute = map(int, pass_data["end_time"].split(':'))
            am_pm = "AM" if hour < 12 else "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            formatted_pass["end_time"] = f"{hour}:{minute:02d} {am_pm}"
        
        return formatted_pass

    def convert_to_utc(self, pass_data):
        """Convert local times to UTC (assuming IST GMT+5:30)"""
        # This is a simplified conversion assuming a fixed offset
        # In a real app, you would use pytz and the user's timezone
        formatted_pass = pass_data.copy()
        
        # Define offset from IST to UTC (5 hours and 30 minutes)
        offset_hours = 5
        offset_minutes = 30
        
        # Helper function to convert time
        def convert_time(time_str):
            if ":" in time_str:
                hour, minute = map(int, time_str.split(':'))
                # Subtract the offset
                utc_hour = hour - offset_hours
                utc_minute = minute - offset_minutes
                
                # Handle minute underflow
                if utc_minute < 0:
                    utc_minute += 60
                    utc_hour -= 1
                
                # Handle hour underflow (day change)
                if utc_hour < 0:
                    utc_hour += 24
                    # Note: date would change too, but we're simplifying here
                
                return f"{utc_hour:02d}:{utc_minute:02d}"
            return time_str
        
        # Extract date and time parts
        date_parts = pass_data["date"].split()
        if len(date_parts) == 2:
            date, time = date_parts
            utc_time = convert_time(time)
            formatted_pass["date"] = f"{date} {utc_time} UTC"
        
        # Convert max_time
        formatted_pass["max_time"] = convert_time(pass_data["max_time"]) + " UTC"
        
        # Convert end_time
        formatted_pass["end_time"] = convert_time(pass_data["end_time"]) + " UTC"
        
        return formatted_pass

    def extract_satellite_passes(self, html_data):
        """
        Extracts satellite pass details from HTML.
        """
        soup = BeautifulSoup(html_data, "html.parser")
        
        # Find the table with the passes data
        passes_table = None
        for table in soup.find_all("table"):
            headers = table.find_all("th")
            if headers and any("Start" in th.text for th in headers) and any("Max altitude" in th.text for th in headers):
                passes_table = table
                break
                
        if not passes_table:
            return []
            
        rows = passes_table.find_all("tr")[2:]  # Skip the header rows
        
        extracted_passes = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 8:
                continue
                
            # Get the background color to determine visibility
            visibility = "not-visible"
            if row.get('style') and 'background-color' in row.get('style').lower():
                bg_color = row.get('style').lower()
                if '#ffffcc' in bg_color:
                    visibility = "marginal"
                elif '#ccffcc' in bg_color:
                    visibility = "good"
                elif '#ffcc99' in bg_color:
                    visibility = "excellent"
            
            date_time = cols[0].text.strip() if cols[0] else ""
            start_az = cols[1].text.strip() if cols[1] else ""
            max_time = cols[2].text.strip() if cols[2] else ""
            max_az = cols[3].text.strip() if cols[3] else ""
            elevation = cols[4].text.strip() if len(cols) > 4 else ""
            end_time = cols[5].text.strip() if len(cols) > 5 else ""
            end_az = cols[6].text.strip() if len(cols) > 6 else ""
            magnitude = cols[7].text.strip() if len(cols) > 7 else ""
            
            info = "Map and details"
            if len(cols) > 8 and cols[8].find("a"):
                info = cols[8].find("a").text.strip()
            
            pass_data = {
                "date": date_time,
                "start_az": start_az,
                "max_time": max_time,
                "max_az": max_az,
                "elevation": elevation,
                "end_time": end_time,
                "end_az": end_az,
                "magnitude": magnitude,
                "info": info,
                "visibility": visibility
            }
            extracted_passes.append(pass_data)
            
        return extracted_passes
    
    
