import json
import os
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Pydantic schema constrains Gemini's output to this exact structure
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
    
    print("Sending text to Gemini for analysis...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': LayoffEvent,
            },
        )
        
        # SDK parses the schema-constrained JSON response directly into a dict
        extracted_data = response.parsed.model_dump() 
        return extracted_data
        
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

if __name__ == "__main__":
    test_article = "Seattle-based Amazon is reportedly slashing 9,000 roles across its AWS and Twitch divisions. The CEO cited a need for streamlining operations and massive restructuring after rapid pandemic hiring."
    
    result = extract_layoff_info(test_article)
    
    print("\nExtraction complete. Structured output:")
    print(json.dumps(result, indent=2))
