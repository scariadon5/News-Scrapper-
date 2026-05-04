import json
import os
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load the hidden .env file
load_dotenv()

# Pull the key securely
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 2. Define the exact structure using Pydantic
# This acts as an unbreakable blueprint for the AI to follow
class LayoffEvent(BaseModel):
    company: str = Field(description="Name of the company.")
    number_laid_off: int = Field(description="The exact number as an integer. (If only a percentage is given, output 0).")
    reason: str = Field(description="Categorize strictly as 'AI', 'Restructuring', 'Cost-cutting', or 'Other'.")

def extract_layoff_info(article_text):
    """Sends news text to Gemini 2.5 Flash and forces a structured JSON response."""
    
    prompt = f"""
    You are a data extraction bot. Read the following news article snippet and extract the layoff event.
    
    News Snippet:
    "{article_text}"
    """
    
    print("Sending text to Gemini for analysis using the new SDK...")
    
    try:
        # We use the newest flash model and pass our LayoffEvent blueprint
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': LayoffEvent,
            },
        )
        
        # The new SDK automatically parses the JSON text into a Python dictionary for us
        extracted_data = response.parsed.model_dump() 
        return extracted_data
        
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

# --- Testing the Extractor ---
if __name__ == "__main__":
    test_article = "Seattle-based Amazon is reportedly slashing 9,000 roles across its AWS and Twitch divisions. The CEO cited a need for streamlining operations and massive restructuring after rapid pandemic hiring."
    
    result = extract_layoff_info(test_article)
    
    print("\nExtraction Complete! Here is the structured output:")
    print(json.dumps(result, indent=2))