import google.generativeai as genai

# Replace with your actual Google Gemini API key
API_KEY = "AIzaSyCjcGLFJBkmKOSc3lb2LPZVI7506uODLWw"

# Configure the API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def chat_with_gemini(prompt):
    """Sends a prompt to Gemini API and returns the response."""
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("Welcome to the Google Gemini Chatbot! Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        
        response = chat_with_gemini(user_input)
        print("Chatbot:", response)
