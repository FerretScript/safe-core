import requests
import json

class GeminiAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_content(self, prompt_text):
        """Method to generate content using the Gemini API."""
        url = f"{self.api_url}?key={self.api_key}"
        
        # The payload based on your provided curl command
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
        
        # Send the POST request
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        
        # Return the response as JSON
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}

# Example usage:
if __name__ == "__main__":
    api_key = 'AIzaSyCIivk7S67LP9YS7pW51JQHS4ZRrizB_iA'  # Your API Key

    gemini_client = GeminiAPIClient(api_key)
    
    # Call the API with a sample prompt
    prompt_text = "Explain how AI works"
    result = gemini_client.generate_content(prompt_text)
    
    print(json.dumps(result, indent=2))  # Pretty print the result
