# Global Layoff Tracker (AI-Powered News Scraper)

An automated data pipeline that continuously monitors global news for company layoffs, extracts the exact metrics using an LLM, deduplicates the data, and exports it to a clean Excel dashboard.

## How It Works

Instead of relying on fragile web scrapers and complex HTML parsing, this pipeline uses **Google's Gemini 2.5 Flash** to semantically understand news articles.

1. **Ingestion** — fetches live articles using `gnews` based on specific boolean search queries (e.g. `layoffs OR "jobs cut" OR "workforce reduction"`).
2. **Extraction** — passes the article text to Gemini via the `google-genai` SDK. The LLM is constrained via Pydantic to strictly output a JSON object containing the `Company Name`, `Number Laid Off`, and the `Reason` (AI, Restructuring, Cost-cutting, or Other).
3. **Deduplication** — uses `thefuzz` for fuzzy string matching to ensure that "Alphabet Inc." and "Google" reporting the same numbers are not logged twice.
4. **Storage** — saves the clean data into a local SQLite database to prevent corruption during continuous runs, and automatically exports a formatted `.xlsx` file for easy reading.

## Tech Stack

- **Language:** Python 3.12+
- **Data Ingestion:** `gnews`
- **AI Extraction:** `google-genai` (Gemini 2.5 Flash), `pydantic`
- **Data Processing:** `thefuzz` (fuzzy matching), `pandas`
- **Storage:** `sqlite3`, `openpyxl`

## Local Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/scariadon5/News-Scrapper-.git
cd News-Scrapper-
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

**4. Run the pipeline**
```bash
python main.py
```

This fetches recent layoff-related articles, runs them through Gemini for structured extraction, deduplicates against existing entries, saves everything to `global_layoffs.db`, and exports the results to `layoffs_master_list.xlsx`.

## Sample Output

The repo includes a sample `global_layoffs.db` and `layoffs_master_list.xlsx` generated from a past pipeline run, so you can inspect the output format without running it yourself first.

## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

---

Built by [Don Scaria](https://github.com/scariadon5)
