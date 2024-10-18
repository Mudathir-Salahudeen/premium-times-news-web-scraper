import pytest
from unittest.mock import patch, Mock
import requests  
from scraper.article_scraper import scrape_news, scrape_article_details

BASE_URL = "https://www.premiumtimesng.com/category/business/business-news"

def test_scrape_news_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = """
        <html>
            <body>
                <article class="jeg_post">
                    <h3 class="jeg_post_title">
                        <a href="https://example.com/news1">News Title 1</a>
                    </h3>
                    <div class="jeg_post_excerpt">Summary of news 1</div>
                    <div class="jeg_meta_author">by Author 1</div>
                    <div class="jeg_meta_date">Date 1</div>
                    <img data-src="https://example.com/image1.jpg" src="image1.jpg">
                </article>
                <article class="jeg_post">
                    <h3 class="jeg_post_title">
                        <a href="https://example.com/news2">News Title 2</a>
                    </h3>
                    <div class="jeg_post_excerpt">Summary of news 2</div>
                    <div class="jeg_meta_author">by Author 2</div>
                    <div class="jeg_meta_date">Date 2</div>
                    <img data-src="https://example.com/image2.jpg" src="image2.jpg">
                </article>
            </body>
        </html>
    """

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        results = scrape_news()

    assert len(results) == 2
    assert results[0]['title'] == "News Title 1"
    assert results[0]['link'] == "https://example.com/news1"
    assert results[1]['title'] == "News Title 2"
    assert results[1]['link'] == "https://example.com/news2"


def test_scrape_news_failure():
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        results = scrape_news()

    assert results == []


def test_scrape_article_details_success():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = """
        <html>
            <body>
                <h1 class="jeg_post_title">Article Title</h1>
                <h2 class="jeg_post_subtitle">Article Subtitle</h2>
                <div class="jeg_meta_author"><a>Author Name</a></div>
                <div class="jeg_meta_date"><a>Date</a></div>
                <div class="jeg_featured"><img src="https://example.com/image.jpg"></div>
                <div class="jeg_inner_content">
                    <p>This is the first paragraph of the article.</p>
                    <p>Support PREMIUM TIMES' journalism.</p>
                    <p>This is another paragraph.</p>
                </div>
            </body>
        </html>
    """

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        result = scrape_article_details("https://example.com/news1")

    assert result['title'] == "Article Title"
    assert result['subtitle'] == "Article Subtitle"
    assert result['author'] == "Author Name"
    assert result['date'] == "Date"
    assert result['image_url'] == "https://example.com/image.jpg"
    assert result['full_article'] == "This is the first paragraph of the article.\n\nThis is another paragraph."


def test_scrape_article_details_failure():
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        result = scrape_article_details("https://example.com/news1")

    assert 'error' in result
    assert "Failed to retrieve the article" in result['error']
