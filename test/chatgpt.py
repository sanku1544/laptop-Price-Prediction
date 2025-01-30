import openai
import os

# Load your OpenAI API key from an environment variable
openai.api_key = "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"  # Replace with your OpenAI API key

def chat_with_bot(user_input):
    # Send a request to OpenAI's GPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150  # Controls the length of the response
    )
    
    # Get the response text
    return response['choices'][0]['message']['content']

def main():
    print("Welcome to the Simple Chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        # Get the response from the bot
        bot_response = chat_with_bot(user_input)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    main()
