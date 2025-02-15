
import os
from flask import Flask, jsonify, request, send_from_directory
import csv
# from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# CORS(app)

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


@app.route('/api')
def read_root():
    return jsonify({
                       "message": "Welcome to the News API! Use /articles to get a list of articles or /articles/<id> to get a specific article."})


@app.route('/api/articles', methods=['GET'])
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


@app.route('/api/articles/<int:id>', methods=['GET'])
def get_article(id):
    article = next((article for article in articles if article["ID"] == id), None)
    if article:
        return jsonify(article)
    return jsonify({"error": "Article not found"}), 404


@app.route('/api/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()
    filtered_articles = [article for article in articles if
                         keyword in article["Title"].lower() or keyword in article["Summary"].lower()]
    return jsonify(filtered_articles)

@app.route("/")
@app.route('/<path:path>')
def catch_all(path=None):
    return send_from_directory(app.static_folder,'index.html')
    
if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=7000,debug=True)
    app.run(debug=True)


