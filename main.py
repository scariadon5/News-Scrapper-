from gnews import GNews
import time

from extractor import extract_layoff_info
from database import insert_layoff_record, export_to_excel

def fetch_and_process_news():
    print("Fetching latest news regarding layoffs...")
    
    # Limited to 10 articles per run to stay within Gemini's free-tier rate limit
    google_news = GNews(language='en', country='US', period='7d', max_results=10)
    articles = google_news.get_news('layoffs OR "jobs cut" OR "workforce reduction"')
    
    if not articles:
        print("No recent articles found.")
        return

    print(f"Found {len(articles)} articles. Starting AI extraction...")
    print("-" * 40)

    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')
        
        # Combine title and description to give the model enough context to extract from
        text_to_analyze = f"Headline: {title}\nSummary: {description}"
        
        print(f"Analyzing: {title[:60]}...")
        extracted_data = extract_layoff_info(text_to_analyze)
        
        if extracted_data and extracted_data.get('number_laid_off', 0) > 0:
            company = extracted_data['company']
            count = extracted_data['number_laid_off']
            reason = extracted_data['reason']
            insert_layoff_record(company, count, reason, url)
        else:
            print(" -> No specific layoff numbers found in this article snippet. Skipping.")
            
        # Gemini free tier caps at 15 requests/minute
        time.sleep(4)

    print("-" * 40)
    print("Pipeline run complete!")
    export_to_excel()

if __name__ == "__main__":
    fetch_and_process_news()
