from readability import Document
from bs4 import BeautifulSoup
import requests

class WebScraper:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

def scrape(self, url: str):

    try:
        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            return None
        
        if "text/html" not in response.headers.get("Content-Type", ""):
            return None

        doc = Document(response.text)

        title = doc.short_title()

        main_html = doc.summary()

        soup = BeautifulSoup(main_html, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        if len(text) < 350:
            return None

        return {
            "url": url,
            "title": title,
            "text": text.strip()
        }

    except Exception as e:
        print("Scraping error:", e)
        return None