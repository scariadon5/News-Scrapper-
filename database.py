import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "global_layoffs.db"

def setup_database():
    """Creates the SQLite database and the layoffs table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS layoffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            layoff_count INTEGER,
            reason TEXT,
            source_url TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

def insert_layoff_record(company, count, reason, source_url):
    """Inserts a single extracted layoff event into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Parameterized query to avoid SQL injection
    cursor.execute('''
        INSERT INTO layoffs (company, layoff_count, reason, source_url)
        VALUES (?, ?, ?, ?)
    ''', (company, count, reason, source_url))
    
    conn.commit()
    conn.close()
    print(f"Successfully added: {company} ({count} layoffs).")

def export_to_excel(filename="layoffs_master_list.xlsx"):
    """Reads the SQLite database and exports it to a formatted Excel file."""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM layoffs", conn)
        df.to_excel(filename, index=False, engine='openpyxl')
        conn.close()
        print(f"Success: Database exported to {filename}")
    except Exception as e:
        print(f"Error exporting to Excel: {e}")

if __name__ == "__main__":
    # Quick smoke test: seed a few rows and confirm the export path works
    setup_database()
    
    insert_layoff_record("Google", 1000, "Restructuring", "https://news.example.com/google")
    insert_layoff_record("Discord", 170, "AI", "https://news.example.com/discord")
    insert_layoff_record("Twitch", 500, "Cost-cutting", "https://news.example.com/twitch")
    
    export_to_excel()
