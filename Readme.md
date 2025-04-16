
# 📰 News Data Ingestion Script

This project fetches the latest **technology news** every hour using the **NewsAPI**, and saves it in three different formats: CSV, SQLite (a mini database), and JSON. It uses Python and runs automatically in the background using a **cron job** (like a scheduled task).

---

## 📜 What this project does — Layman Speak

This script is like a virtual assistant that:

1. **Grabs latest tech news** online (from NewsAPI)
2. **Cleans up the information** so it’s easy to work with
3. **Saves the news in 3 formats**:
   - Excel-like file (CSV)
   - Database file (SQLite)
   - Archive file (JSON)
4. **Skips any duplicates**
5. **Runs every hour**, without needing your help

---

## 🧠 Full Python Code (Ingests Tech News)

```python
import requests
import pandas as pd
import sqlite3
from datetime import datetime
import os
import json

# Load API Key
def load_api_key(path='api_keys.txt'):
    with open(path, 'r') as f:
        for line in f:
            if 'NEWS_API_KEY' in line:
                return line.strip().split('=')[1]

api_key = "4329bed58eed43438a4d6ebeaad4e4f3"  # Or use: load_api_key()
category = "technology"
country = "us"

# Fetch Articles from News API
url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
response = requests.get(url)
articles = response.json().get("articles", [])

# Flatten 'source' field
for article in articles:
    if isinstance(article.get('source'), dict):
        article['source'] = article['source'].get('name', '')
        article['category'] = category
        article['country'] = country

# Convert to DataFrame
df = pd.DataFrame(articles)

# Save to CSV
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
csv_file = f"/Applications/XAMPP/xamppfiles/htdocs/news/batch_output/{category}_{country}_{now}.csv"
df.to_csv(csv_file, index=False)
print(f"✅ CSV saved: {csv_file}")

# Save to SQLite
conn = sqlite3.connect('tech_news.db')
cursor = conn.cursor()
cursor.execute("SELECT url FROM batch_news")
existing_urls = set(row[0] for row in cursor.fetchall())
df_filtered = df[~df['url'].isin(existing_urls)]
df_filtered.to_sql('batch_news', conn, if_exists='append', index=False)
conn.close()
print("✅ Saved to SQLite: tech_news.db")

# Save to JSON (append only new articles)
json_file = f"/Applications/XAMPP/xamppfiles/htdocs/news/batch_output/output.json"
if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
    with open(json_file, "r") as f:
        existing_data = json.load(f)
else:
    existing_data = []

existing_urls = {article["url"] for article in existing_data if "url" in article}
new_articles = [a for a in articles if "url" in a and a["url"] not in existing_urls]
existing_data.extend(new_articles)

with open(json_file, "w") as f:
    json.dump(existing_data, f, indent=4)

print(f"✅ JSON updated: {json_file}")
```

---

## 📁 Project Structure

```
news/
├── batch_ingest.py       # This script fetches and saves the news
├── api_keys.txt          # File with your News API key (optional)
├── batch_output/         # Folder where CSV and JSON are saved
├── tech_news.db          # SQLite database file
├── logfile.log           # Logs every run from cron
└── README.md             # You’re reading this!
```

---

## ⚙️ Setup Steps

### 1. Install Python Packages

```bash
python3 -m pip install pandas requests --break-system-packages
```

### 2. Add Your API Key

Create a file called `api_keys.txt` and paste this line inside:

```
NEWS_API_KEY=your_api_key_here
```

(If you're using the hardcoded key, skip this step.)

### 3. Test the Script

```bash
python3 batch_ingest.py
```

Check the output files in `batch_output/`, and make sure the SQLite database was updated too.

---

## ⏰ Automate It (Run Every Hour)

### Open the crontab

```bash
crontab -e
```

### Add this line

```bash
0 * * * * /usr/local/bin/python3 /Applications/XAMPP/xamppfiles/htdocs/news/batch_ingest.py >> /Applications/XAMPP/xamppfiles/htdocs/news/logfile.log 2>&1
```

✅ Now the script will run **once every hour**, and write logs to `logfile.log`.

---

## 🛑 Pause the Cron Job

If you want to stop it temporarily:

1. Run `crontab -e`
2. Add `#` at the beginning of the line to comment it out

---

## 🐞 Common Issues (Layman Tips)

### 🧩 `No module named 'pandas'`
Run:

```bash
/usr/local/bin/python3 -m pip install pandas requests --break-system-packages
```

### 🧩 `FileNotFoundError: api_keys.txt`
Create a file named `api_keys.txt` and add:

```
NEWS_API_KEY=your_actual_key_here
```

Make sure it’s in the **same folder** as the Python script.

---

## ✅ Output Summary

- ✅ CSV in `batch_output/`
- ✅ JSON archive in `batch_output/output.json`
- ✅ SQLite database in `tech_news.db`
- ✅ Logs in `logfile.log`

---

## 🤖 Final Words — Layman Speak

Imagine having a robot that:
- Visits a news site every hour
- Picks up only new headlines
- Writes them in Excel, database, and archive file
- Avoids saving duplicates
- And never forgets to do this — every single hour!

That’s exactly what this script does for you. Set it once. Forget it. Let the news flow!

---

## 💬 Questions?

Just ping me!
