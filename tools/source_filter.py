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

            # enforce domain limit
            if domain_counts.get(domain, 0) >= self.max_sources_per_domain:
                continue

            seen_urls.add(url)

            domain_counts[domain] = domain_counts.get(domain, 0) + 1

            r["preferred"] = self._is_preferred(domain)

            filtered.append(r)

        filtered.sort(key=lambda x: x["preferred"], reverse=True)

        return filtered