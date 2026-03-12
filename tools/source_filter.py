from typing import List, Dict
from urllib.parse import urlparse


class SourceFilter:

    def __init__(self):

        self.blocked_domains = {
            "pinterest.com",
            "quora.com",
            "reddit.com",
            "facebook.com",
            "instagram.com",
            "tiktok.com",
            "linkedin.com"
        }

        self.preferred_domains = {
            "wikipedia.org",
            "investopedia.com",
            "reuters.com",
            "bbc.com",
            "nature.com",
            "sciencedirect.com",
            "gov",
            "edu"
        }
        # SEO KEYWORDS TO IDENTIFY COMMERCIAL INTENT IN QUERIES
        self.seo_keywords = {
            "top",
            "best",
            "buy",
            "deal",
            "coupon",
            "discount",
            "review",
            "vs",
            "comparison",
            "affiliate"
        }
        # limit to 2 sources per domain to ensure diversity
        self.max_sources_per_domain = 2   

    def _extract_domain(self, url: str) -> str:
        return urlparse(url).netloc.lower()

    def _is_blocked(self, domain: str) -> bool:

        for blocked in self.blocked_domains:
            if blocked in domain:
                return True

        return False

    def _is_preferred(self, domain: str) -> bool:

        for preferred in self.preferred_domains:
            if preferred in domain:
                return True

        return False
    
    def _is_seo_spam(self, url: str) -> bool:

        url_lower = url.lower()

        for keyword in self.seo_keywords:
            if f"/{keyword}" in url_lower:
                return True

        return False

    def filter(self, results: List[Dict]) -> List[Dict]:

        filtered = []
        seen_urls = set()
        #TRACK DOMAIN FREQUENCY
        domain_counts = {}   

        for r in results:

            url = r["url"]

            if url in seen_urls:
                continue

            domain = self._extract_domain(url)

            if self._is_blocked(domain):
                continue

            if self._is_seo_spam(url): # seo spam check
                continue

            # enforce domain limit
            if domain_counts.get(domain, 0) >= self.max_sources_per_domain:
                continue

            seen_urls.add(url)

            domain_counts[domain] = domain_counts.get(domain, 0) + 1

            r["preferred"] = self._is_preferred(domain)

            filtered.append(r)

        filtered.sort(key=lambda x: x["preferred"], reverse=True)

        return filtered