# from fastapi import FastAPI, HTTPException, Query
# from typing import List, Optional
# import csv
# from datetime import datetime
#
# app = FastAPI()
#
# # Load articles from CSV
# def read_articles_from_csv():
#     articles = []
#     try:
#         with open('news_articles.csv', mode='r', encoding='utf-8') as infile:
#             reader = csv.DictReader(infile)
#             for row in reader:
#                 articles.append({
#                     "ID": row["ID"],
#                     "Title": row["Title"],
#                     "Summary": row["Summary"],
#                     "Published Date": row["Published Date"],
#                     "URL": row["URL"],
#                     "Source": row["Source"],
#                     "Category": row["Category"]
#                 })
#     except Exception as e:
#         print(f"Error reading CSV: {e}")
#     return articles
#
# articles = read_articles_from_csv()
#
# @app.get("/", response_model=dict)
# def read_root():
#     return {"message": "Welcome to the News API! Use /articles t get a list of articles or /articles/{id} to get a specific article."}
#
# @app.get("/articles", response_model=List[dict])
# def get_articles(start_date: Optional[str] = None, end_date: Optional[str] = None, category: Optional[str] = None):
#     filtered_articles = articles
#     if start_date:
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         filtered_articles = [article for article in filtered_articles if datetime.strptime(article["Published Date"], "%Y-%m-%d %H:%M:%S") >= start_date]
#     if end_date:
#         end_date = datetime.strptime(end_date, "%Y-%m-%d")
#         filtered_articles = [article for article in filtered_articles if datetime.strptime(article["Published Date"], "%Y-%m-%d %H:%M:%S") <= end_date]
#     if category:
#         filtered_articles = [article for article in filtered_articles if article["Category"].lower() == category.lower()]
#     return filtered_articles
#
# @app.get("/articles/{id}", response_model=dict)
# def get_article(id: int):
#     try:
#         article = next(article for article in articles if int(article["ID"]) == id)
#         return article
#     except StopIteration:
#         raise HTTPException(status_code=404, detail="Article not found")
#
# @app.get("/search", response_model=List[dict])
# def search_articles(keyword: str):
#     keyword = keyword.lower()
#     filtered_articles = [article for article in articles if keyword in article["Title"].lower() or keyword in article["Summary"].lower()]
#     return filtered_articles
#

from flask import Flask, jsonify, request
import csv
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load articles from CSV
def read_articles_from_csv():
    articles = []
    try:
        with open('news_articles.csv', mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                articles.append({
                    "ID": int(row["ID"]),
                    "Title": row["Title"],
                    "Summary": row["Summary"],
                    "Published Date": row["Published Date"],
                    "URL": row["URL"],
                    "Source": row["Source"],
                    "Category": row["Category"]
                })
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return articles
articles = read_articles_from_csv()


@app.route('/')
def read_root():
    return jsonify({
                       "message": "Welcome to the News API! Use /articles to get a list of articles or /articles/<id> to get a specific article."})


@app.route('/articles', methods=['GET'])
def get_articles():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    category = request.args.get('category')

    # Convert dates only if provided
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

    # Filter in one loop for better efficiency
    def filter_article(article):
        pub_date = datetime.strptime(article["Published Date"], "%Y-%m-%d %H:%M:%S")
        if start_date and pub_date < start_date:
            return False
        if end_date and pub_date > end_date:
            return False
        if category and article["Category"].lower() != category.lower():
            return False
        return True

    filtered_articles = list(filter(filter_article, articles))

    return jsonify(filtered_articles)


@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    article = next((article for article in articles if article["ID"] == id), None)
    if article:
        return jsonify(article)
    return jsonify({"error": "Article not found"}), 404


@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()
    filtered_articles = [article for article in articles if
                         keyword in article["Title"].lower() or keyword in article["Summary"].lower()]
    return jsonify(filtered_articles)


if __name__ == '__main__':
    app.run(debug=True)


# http://127.0.0.1:5000/\search?keyword=political

