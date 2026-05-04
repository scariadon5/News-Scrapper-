from gnews import GNews
import time

# Import the functions from the files you just built!
from extractor import extract_layoff_info
from database import insert_layoff_record, export_to_excel

def fetch_and_process_news():
    print("Fetching latest news regarding layoffs...")
    
    # Configure the news scraper to look at the last 7 days, limit to 10 articles for testing
    google_news = GNews(language='en', country='US', period='7d', max_results=10)
    
    # The exact search query
    articles = google_news.get_news('layoffs OR "jobs cut" OR "workforce reduction"')
    
    if not articles:
        print("No recent articles found.")
        return

    print(f"Found {len(articles)} articles. Starting AI extraction...")
    print("-" * 40)

    for article in articles:
        # 1. Get the article details
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        
        # Combine title and description to give the AI enough context
        text_to_analyze = f"Headline: {title}\nSummary: {description}"
        
        print(f"Analyzing: {title[:60]}...")
        
        # 2. Pass the text to your Gemini Extractor
        extracted_data = extract_layoff_info(text_to_analyze)
        
        # 3. If Gemini successfully found a layoff event AND the number isn't 0
        if extracted_data and extracted_data.get('number_laid_off', 0) > 0:
            
            company = extracted_data['company']
            count = extracted_data['number_laid_off']
            reason = extracted_data['reason']
            
            # 4. Save it to the database
            insert_layoff_record(company, count, reason, url)
            
        else:
            print(" -> No specific layoff numbers found in this article snippet. Skipping.")
            
        # Pause for 4 seconds to respect the Gemini Free Tier limits (15 requests per minute)
        time.sleep(4)

    print("-" * 40)
    print("Pipeline run complete!")
    
    # Export the final results to Excel
    export_to_excel()

# --- Run the Pipeline ---
if __name__ == "__main__":
    fetch_and_process_news()