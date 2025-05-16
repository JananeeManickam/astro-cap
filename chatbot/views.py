# chatbot/views.py
import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
from rest_framework.permissions import AllowAny


class AstronomyChatbotView(APIView):
    permission_classes = [AllowAny]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure Gemini API 
        genai.configure(api_key="AIzaSyD3lNxKVfPt62OQaXlfwqEIkmiWN_YMrxw")
        
        # Use the correct model initialization
        self.text_model = genai.GenerativeModel("gemini-1.5-flash")
        self.image_model = genai.GenerativeModel("gemini-1.5-flash")

    def process_text_query(self, message):
        """
        Process text-only astronomy queries
        """
        prompt = f"""You are an astronomy-focused chatbot. 
        Only answer questions briefly (in 2 to 4 lines) related to astronomy, 
        astrophysics, space exploration, celestial bodies, 
        and cosmic phenomena. NOTE: If the query is not related to astronomy, 
        strictly decline to answer and acknowledge them.

        Question: {message}
        
        Provide a brief, informative answer."""

        response = self.text_model.generate_content(prompt)
        return response.text

    def process_image_query(self, image_file, message=''):
        """
        Process image-based astronomy queries
        """
        # Open the image
        try:
            image = Image.open(image_file)
        except Exception as e:
            return f"Error processing image: {str(e)}"

        # Prepare the prompt
        prompt_text = message or "Describe this astronomical image in brief (in 4 to 6 lines). Identify any celestial objects, phenomena, or interesting features."

        # Generate content with both image and text
        try:
            response = self.image_model.generate_content([
                prompt_text,
                image
            ])
            return response.text
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def post(self, request):
        # Check if an image is uploaded
        image_file = request.FILES.get('image')
        message = request.data.get('message', '')

        print("-"*90)
        print("Received message:", message)
        print("Received image:", bool(image_file))

        try:
            # Case 1: Image and text query
            if image_file and message:
                bot_response = self.process_image_query(image_file, message)
            
            # Case 2: Image-only query
            elif image_file:
                bot_response = self.process_image_query(image_file)
            
            # Case 3: Text-only query
            elif message:
                bot_response = self.process_text_query(message)
            
            # Case 4: No input
            else:
                bot_response = "Please provide either a text message or an image to analyze."

            print("Generated response:", bot_response)
            print("-"*90)

            return Response({
                'message': bot_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        # Simple clear method (no user or session tracking)
        return Response(status=status.HTTP_204_NO_CONTENT)