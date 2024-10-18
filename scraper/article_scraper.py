import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.premiumtimesng.com/category/business/business-news"


def scrape_news():
    try:
        # Send a request to the webpage
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all news list blocks
        news_items = soup.find_all(
            "article", class_="jeg_post"
        )  # Adjust class as needed
        results = []  # List to hold the news data

        # Loop through each news item and extract relevant details
        for news_item in news_items:
            try:
                title_tag = news_item.find("h3", class_="jeg_post_title")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find("a")["href"]

                    summary = news_item.find("div", class_="jeg_post_excerpt").get_text(
                        strip=True
                    )
                    author = (
                        news_item.find("div", class_="jeg_meta_author")
                        .get_text(strip=True)
                        .replace("by", "")
                        .strip()
                    )
                    date = news_item.find("div", class_="jeg_meta_date").get_text(
                        strip=True
                    )

                    img_tag = news_item.find("img")
                    img_url = (
                        img_tag.get("data-src", img_tag.get("src"))
                        if img_tag
                        else "No image available"
                    )

                    # Append the data to results
                    results.append(
                        {
                            "title": title,
                            "link": link,
                            "summary": summary,
                            "author": author,
                            "date": date,
                            "image_url": img_url,
                        }
                    )
                else:
                    print("Could not find title tag for this news item.")
            except Exception as e:
                print(f"An error occurred while processing a news item: {e}")

        return results

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return []


def scrape_article_details(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extracting title
        title = (
            soup.find("h1", class_="jeg_post_title").get_text(strip=True)
            if soup.find("h1", class_="jeg_post_title")
            else "Title not found"
        )

        # Extracting subtitle
        subtitle = (
            soup.find("h2", class_="jeg_post_subtitle").get_text(strip=True)
            if soup.find("h2", class_="jeg_post_subtitle")
            else "Subtitle not found"
        )

        # Extracting author
        author = (
            soup.find("div", class_="jeg_meta_author").find("a").get_text(strip=True)
            if soup.find("div", class_="jeg_meta_author")
            else "Author not found"
        )

        # Extracting date
        date = (
            soup.find("div", class_="jeg_meta_date").find("a").get_text(strip=True)
            if soup.find("div", class_="jeg_meta_date")
            else "Date not found"
        )

        # Extracting image URL
        image_url = (
            soup.find("div", class_="jeg_featured").find("img")["src"]
            if soup.find("div", class_="jeg_featured").find("img")
            else "Image URL not found"
        )

        # Extracting article content
        body_content = soup.find("div", class_="jeg_inner_content")
        if body_content:
            # Get all paragraphs from the body content, ensuring to avoid unwanted text
            unwanted_phrases = [
                "Support PREMIUM TIMES' journalism",
                "consider supporting us",
                "Help us maintain free and accessible news",
                "TEXT AD",
                "high-quality journalism.",
                "readership",
                "prohibitive",
                "paywall",
            ]

            paragraphs = [
                p.get_text(strip=True)
                for p in body_content.find_all("p")
                if p.get_text(strip=True)
                and not any(
                    phrase in p.get_text(strip=True) for phrase in unwanted_phrases
                )
            ]

            # Join all paragraphs into a single article
            full_article = (
                "\n\n".join(paragraphs) if paragraphs else "No content available."
            )
        else:
            full_article = "Body content not found"

        # Return the extracted information as a dictionary
        return {
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "date": date,
            "image_url": image_url,
            "full_article": full_article,
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve the article: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
