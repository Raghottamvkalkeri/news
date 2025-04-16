import json
import pandas as pd
import re

# Load uploaded JSON file
with open("batch_output/output.json", "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Fill missing values
df['author'] = df['author'].fillna("Unknown")
df['description'] = df['description'].fillna("No Description")

# Drop irrelevant columns if present
columns_to_drop = ["content", "urlToImage"]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Clean text fields
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

df['title'] = df['title'].apply(clean_text)
df['description'] = df['description'].apply(clean_text)

# Remove duplicates by 'url'
df = df.drop_duplicates(subset="url")

# Convert publishedAt to datetime if present
if 'publishedAt' in df.columns:
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')

# Save cleaned data
cleaned_json_path = "cleaned_output.json"
cleaned_csv_path = "cleaned_output.csv"

df.to_json(cleaned_json_path, orient="records", indent=4)
df.to_csv(cleaned_csv_path, index=False)

cleaned_json_path, cleaned_csv_path