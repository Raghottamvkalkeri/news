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

api_key = load_api_key() 
category = "sports"
country = "us"
# Fetch Articles from News API
url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
response = requests.get(url)
articles = response.json().get("articles", [])

# Flatten 'source' field (from dict to just source name)
for article in articles:
    if isinstance(article.get('source'), dict):
        article['source'] = article['source'].get('name', '')
        article['category'] = category
        article['country']= country

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

# check if data exists in the table
cursor.execute("Select url from batch_news")
existing_urls = set(row[0] for row in cursor.fetchall())

# Filter out duplicates from DataFrame
df_filtered = df[~df['url'].isin(existing_urls)]



# cursor.execute("ALTER TABLE batch_news ADD COLUMN country TEXT;")
df_filtered.to_sql('batch_news', conn, if_exists='append', index=False)
conn.close()
print("✅ Saved to SQLite: tech_news.db")


# Save to JSON (append to existing file or create if doesn't exist)
json_file = f"/Applications/XAMPP/xamppfiles/htdocs/news/batch_output/output.json"

# Load existing data if file exists
if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
    with open(json_file, "r") as f:
        existing_data = json.load(f)
else:
    existing_data = []

# Create a set of existing URLs to detect duplicates
existing_urls = {article["url"] for article in existing_data if "url" in article}

# Filter out only new (non-duplicate) articles
new_articles = [a for a in articles if "url" in a and a["url"] not in existing_urls]

# Append only unique new articles
existing_data.extend(new_articles)

# Save back to file
with open(json_file, "w") as f:
    json.dump(existing_data, f, indent=4)

print(f"✅ JSON updated: {json_file}")


