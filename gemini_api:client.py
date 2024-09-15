import requests
import json

class GeminiAPIClient:
    def __init__(self, api_key):
        # Initialize the API client with the API key and URL
        self.api_key = api_key
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_content_stream(self, prompt_text):
        """Method to generate content using the Gemini API and stream the response."""
        # Append the API key to the URL for authentication
        url = f"{self.api_url}?key={self.api_key}"
        
        # Construct the payload (the input to the model)
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_text
                        }
                    ]
                }
            ]
        }

        # Send the POST request with streaming enabled
        # stream=True allows the response to be sent in chunks as they are available
        with requests.post(url, headers=self.headers, data=json.dumps(payload), stream=True) as response:
            # Check if the request was successful
            if response.status_code == 200:
                # Start processing the response in chunks
                # `iter_content` allows you to iterate over the response content piece by piece
                for chunk in response.iter_content(chunk_size=None):
                    # Each chunk is received as bytes and needs to be decoded
                    if chunk:
                        # Decode the chunk (from bytes to string) and print it
                        content_chunk = chunk.decode('utf-8')
                        print(content_chunk)
            else:
                # If there's an error (e.g., status code != 200), print the error details
                print({"error": response.status_code, "message": response.text})

# Example usage:
if __name__ == "__main__":
    # Replace this with your actual API key
    api_key = 'AIzaSyCIivk7S67LP9YS7pW51JQHS4ZRrizB_iA'  # Your API Key

    # Initialize the Gemini API client with the API key
    gemini_client = GeminiAPIClient(api_key)
    
    # Define the prompt text (input for content generation)
    prompt_text = "Explain how to make some tortillas de harina"

    # Call the API to generate content using streaming
    gemini_client.generate_content_stream(prompt_text)
