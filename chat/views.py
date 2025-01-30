from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json

# Replace with your actual Google Gemini API key
API_KEY = "AIzaSyCjcGLFJBkmKOSc3lb2LPZVI7506uODLWw"

# Configure the API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

@csrf_exempt  # Disable CSRF for AJAX requests
def chat_with_gemini(request):
    """Handles the chat request and gets a response from Gemini API."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse the request body
            user_input = data.get("userInput", "").strip()

            # Check if the user input is empty
            if not user_input:
                return JsonResponse({"error": "User input cannot be empty."}, status=400)

            # Create contents structure as required by Gemini API
            contents = [{"role": "user", "parts": [{"text": user_input}]}]

            # Get the response from the Gemini API
            response = model.generate_content(contents=contents)
            bot_reply = response.text

            # Return the response as JSON
            return JsonResponse({"bot_reply": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
