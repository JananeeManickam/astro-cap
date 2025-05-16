import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import AstronomicalEvent
from .serializers import AstronomicalEventSerializer
from datetime import datetime
from django.conf import settings
from django.db.utils import DatabaseError
from rest_framework.permissions import AllowAny

class OnThisDateView(APIView):
    permission_classes = [AllowAny]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure Gemini API 
        genai.configure(api_key="AIzaSyD3lNxKVfPt62OQaXlfwqEIkmiWN_YMrxw")
        
        # Use the Gemini model
        self.text_model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_astronomical_events(self, month, day):
        """
        Generate astronomical events for a specific date using Gemini
        """
        prompt = f"""Generate a list of 5-8 unique astronomical events, discoveries, 
        births, or deaths of astronomers and space scientists (with strict full name) that occurred on {month} {day}. 
        Focus strictly on astronomical and space-related events. 
        For each event, provide:
        - A crisp brief description
        - The year it occurred
        - Categorize as DISCOVERY, BIRTH, DEATH, MISSION, or OBSERVATION

        Format each event like this:
        Year: [YYYY]
        Type: [CATEGORY]
        Description: [Event Description]

        Ensure all events are scientifically accurate and space/astronomy related."""
        
        try:
            response = self.text_model.generate_content(prompt)
            return self.parse_astronomical_events(response.text)
        except Exception as e:
            return str(e)

    def parse_astronomical_events(self, response_text):
        """
        Parse the Gemini response into structured astronomical events
        """
        events = []
        current_event = {}
        
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('Year:'):
                if current_event:
                    events.append(current_event)
                current_event = {}
                try:
                    current_event['year'] = int(line.split(':')[1].strip())
                except ValueError:
                    current_event['year'] = 0
            elif line.startswith('Type:'):
                current_event['event_type'] = line.split(':')[1].strip()
            elif line.startswith('Description:'):
                current_event['event_description'] = line.split(':', 1)[1].strip()
        
        # Add the last event
        if current_event:
            events.append(current_event)
        
        return events

    def get_events_for_date(self, month, day):
        """
        Get or generate astronomical events for a specific date
        """
        try:
            # Validate the date
            date_obj = datetime(2000, int(month), int(day))
        except ValueError:
            return None, 'Invalid date provided'

        formatted_month = date_obj.strftime('%B')  # Get month name
        formatted_day = day
        
        # First try to fetch from database if database is configured
        if hasattr(settings, 'DATABASES') and settings.DATABASES.get('default', {}).get('ENGINE'):
            try:
                # Check if we already have events for this date in the database
                today_date = date_obj.date()
                existing_events = AstronomicalEvent.objects.filter(date=today_date)
                
                if existing_events.exists():
                    # Return existing events
                    return [
                        {
                            'year': event.year,
                            'event_type': event.event_type,
                            'event_description': event.event_description,
                            'date': event.date
                        } for event in existing_events
                    ], None
            except (DatabaseError, Exception) as e:
                # If database error occurs, continue to generate events without saving
                print(f"Database error: {e}")
        
        # Generate new events
        events = self.generate_astronomical_events(formatted_month, formatted_day)
        
        # If events are not properly formatted (returned an error string)
        if isinstance(events, str):
            return None, f"Error generating events: {events}"
        
        # Try to save to database if configured
        if hasattr(settings, 'DATABASES') and settings.DATABASES.get('default', {}).get('ENGINE'):
            try:
                saved_events = []
                today_date = date_obj.date()
                
                for event in events:
                    event_data = {
                        'date': today_date,
                        'year': event.get('year', 0),
                        'event_type': event.get('event_type', 'OBSERVATION'),
                        'event_description': event.get('event_description', '')
                    }
                    
                    serializer = AstronomicalEventSerializer(data=event_data)
                    if serializer.is_valid():
                        serializer.save()
                        saved_events.append(serializer.data)
                
                if saved_events:
                    return saved_events, None
            except (DatabaseError, Exception) as e:
                # If database error occurs, return generated events without saving
                print(f"Error saving to database: {e}")
                
        # Return generated events without database interaction
        formatted_events = []
        for event in events:
            formatted_events.append({
                'year': event.get('year', 0),
                'event_type': event.get('event_type', 'OBSERVATION'),
                'event_description': event.get('event_description', ''),
                'date': date_obj.date().isoformat() if hasattr(date_obj.date(), 'isoformat') else str(date_obj.date())
            })
            
        return formatted_events, None

    def get(self, request):
        """
        Handle GET requests to retrieve astronomical events for today's date
        """
        # Get today's date
        today = datetime.now()
        month = today.month
        day = today.day
        
        events, error = self.get_events_for_date(month, day)
        
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'events': events,
            'current_date': {
                'month': month,
                'day': day,
                'month_name': today.strftime('%B')
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests to retrieve astronomical events for a specific date
        """
        month = request.data.get('month')
        day = request.data.get('day')

        if not month or not day:
            return Response({
                'error': 'Please provide both month and day'
            }, status=status.HTTP_400_BAD_REQUEST)

        events, error = self.get_events_for_date(month, day)
        
        if error:
            return Response({
                'error': error
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get month name for the response
        try:
            month_name = datetime(2000, int(month), 1).strftime('%B')
        except ValueError:
            month_name = ""
            
        return Response({
            'events': events,
            'current_date': {
                'month': month,
                'day': day,
                'month_name': month_name
            }
        }, status=status.HTTP_200_OK)

def onthisdate_interface(request):
    """
    Render the HTML interface
    """
    return render(request, 'onthisdate.html')