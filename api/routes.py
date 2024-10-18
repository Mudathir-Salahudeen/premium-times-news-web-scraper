from flask import Blueprint, jsonify, request
from scraper.article_scraper import scrape_news, scrape_article_details

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/news", methods=["GET"])
def get_news():
    news_data = scrape_news()
    if news_data:
        return jsonify(news_data), 200  # Return JSON response with a 200 OK status
    else:
        return (
            jsonify({"error": "No news items found or an error occurred."}),
            500,
        )  # Return error message


@api_bp.route("/api/news/details/<path:url>", methods=["GET"])
def get_article_details(url):
    if not url:
        return jsonify({"error": "URL parameter is required."}), 400

    article_data = scrape_article_details(url)
    if article_data:
        return jsonify(article_data), 200
    else:
        return jsonify({"error": "Failed to retrieve article details."}), 500
