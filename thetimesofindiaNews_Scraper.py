import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import re
import os

# Function to parse relative time
def parse_relative_time(text):
    match = re.match(r'(\d+)\s+(\w+)\s+ago', text)
    if match:
        amount, unit = int(match.group(1)), match.group(2)
        now = datetime.now()
        if unit == 'second':
            return now - timedelta(seconds=amount)
        elif unit == 'minute':
            return now - timedelta(minutes=amount)
        elif unit == 'hour':
            return now - timedelta(hours=amount)
        elif unit == 'day':
            return now - timedelta(days=amount)
        elif unit == 'week':
            return now - timedelta(weeks=amount)
        elif unit == 'month':
            return now - relativedelta(months=amount)
        elif unit == 'year':
            return now - relativedelta(years=amount)
    return None

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Times of India URL
times_url = "https://timesofindia.indiatimes.com/india"
driver.get(times_url)

# Wait for the page to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)
except Exception as e:
    print(f"Error waiting for the page to load: {e}")
    driver.quit()
    exit()

# Get page source and parse with BeautifulSoup
times_page_source = driver.page_source
times_soup = BeautifulSoup(times_page_source, "html.parser")
driver.quit()

# Initialize list to store article data and set for tracking unique articles
times_article_data = []
existing_articles = set()

# CSV file path
csv_file_path = 'news_articles.csv'

# Function to get the next available ID
def get_next_id():
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            ids = [int(row['ID']) for row in reader if row['ID'].isdigit()]
            return max(ids, default=0) + 1
    return 1

# Get the starting ID
next_id = get_next_id()

# Find article links and titles
times_articles = times_soup.find_all('a', href=True, class_='lfn2e')
for article in times_articles:
    try:
        title = article.get_text(strip=True)
        url = article['href']
        if not url.startswith("https"):
            url = "https://timesofindia.indiatimes.com" + url

        # Skip duplicate articles by comparing both title and URL
        if (title, url) in existing_articles:
            continue

        # Fetch the article page
        article_page = requests.get(url)
        if article_page.status_code != 200:
            print(f"Failed to fetch article: {url}")
            continue

        article_soup = BeautifulSoup(article_page.content, 'html.parser')

        # Extract summary
        summary_tag = article_soup.find('p')
        summary = summary_tag.get_text(strip=True) if summary_tag else "No summary available"

        # Extract published date or generate random date
        published_date_tag = article_soup.find('time')
        if published_date_tag:
            relative_time_text = published_date_tag.getText()
            published_date = parse_relative_time(relative_time_text) or datetime.now()
        else:
            random_days = random.randint(1, 365)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            published_date = datetime.now() - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

        # Append the article data with the current ID
        times_article_data.append({
            "ID": next_id,
            "Title": title,
            "Summary": summary,
            "Published Date": published_date.strftime('%Y-%m-%d %H:%M:%S'),
            "URL": url,
            "Source": "Times of India"
        })

        # Increment the ID for the next article
        next_id += 1

        # Add article to the existing articles set to avoid duplicates in further loops
        existing_articles.add((title, url))

    except Exception as e:
        print(f"Error processing article: {e}")

# Write the new data into the CSV file, skipping duplicates
if times_article_data:
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["ID", "Title", "Summary", "Published Date", "URL", "Source"])
        if outfile.tell() == 0:  # If file is empty, write the header
            writer.writeheader()

        writer.writerows(times_article_data)

    print(f"Times of India articles successfully scraped and saved to '{csv_file_path}'")
else:
    print("No new articles found.")








