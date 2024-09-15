import requests
import json

class GeminiAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_content_stream(self, prompt_text):
        """Method to generate content using the Gemini API and stream the response."""
        url = f"{self.api_url}?key={self.api_key}"
        
        # Constructing the payload based on the expected API format
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
        with requests.post(url, headers=self.headers, data=json.dumps(payload), stream=True) as response:
            if response.status_code == 200:
                # Stream the response in chunks
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        # Decode chunk and print
                        content_chunk = chunk.decode('utf-8')
                        print(content_chunk)
            else:
                print({"error": response.status_code, "message": response.text})

# Example usage:
if __name__ == "__main__":
    api_key = 'AIzaSyCIivk7S67LP9YS7pW51JQHS4ZRrizB_iA'  # Your API Key

    gemini_client = GeminiAPIClient(api_key)
    
    # Define the prompt text (simple tortilla recipe example)
    prompt_text = "Explain how to make some tortillas de harina"

    # Generate content with the prompt
    gemini_client.generate_content_stream(prompt_text)
