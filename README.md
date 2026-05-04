# Global Layoff Tracker (AI-Powered News Scraper)

An automated data pipeline that continuously monitors global news for company layoffs, extracts the exact metrics using an LLM, deduplicates the data, and exports it to a clean Excel dashboard.

## How It Works

Instead of relying on fragile web scrapers and complex HTML parsing, this pipeline uses **Google's Gemini 2.5 Flash** to semantically understand news articles. 

1. **Ingestion:** Fetches live articles using `gnews` based on specific boolean search queries.
2. **Extraction:** Passes the article text to Gemini via the `google-genai` SDK. The LLM is restricted via Pydantic to strictly output a JSON object containing the `Company Name`, `Number Laid Off`, and the `Reason` (AI, Restructuring, Cost-cutting, etc.).
3. **Deduplication:** Uses `thefuzz` for fuzzy string matching to ensure that "Alphabet Inc." and "Google" reporting the same numbers are not logged twice.
4. **Storage:** Saves the clean data into a local SQLite database to prevent corruption during continuous runs, and automatically exports a formatted `.xlsx` file for easy reading.

## Tech Stack

* **Language:** Python 3.12+
* **Data Ingestion:** `gnews`
* **AI Extraction:** `google-genai` (Gemini 2.5 Flash), `pydantic`
* **Data Processing:** `thefuzz` (NLP fuzzy matching), `pandas`
* **Storage:** `sqlite3`, `openpyxl`

## Local Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/scariadon5/News-Scrapper-.git](https://github.com/scariadon5/News-Scrapper-.git)
cd News-Scrapper-