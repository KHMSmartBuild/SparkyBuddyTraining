import logging
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from typing import List

import requests
from bs4 import BeautifulSoup


# Define the crawling parameters
MAX_PAGES = 15
MAX_DEPTH = 4
MAX_PAGES_PER_DOMAIN = 8

# Define the output file name
OUTPUT_FILE = "Electrical_Knowledge_output.txt"

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

# Define root domains to crawl
domains = ["theiet.org", "bsria.com", "electricalsafetyfirst.org.uk", "niceic.com", "eca.co.uk", "cibse.org",
           "elecsa.co.uk", "iec.ch", "cityandguilds.com", "electriciansguide.co.uk"]
root_urls = ["https://www.theiet.org/", "https://www.bsria.com/", "https://www.electricalsafetyfirst.org.uk/",
             "https://www.niceic.com/", "https://www.eca.co.uk/", "https://www.cibse.org/",
             "https://www.elecsa.co.uk/", "https://www.iec.ch/", "https://www.cityandguilds.com/",
             "https://www.electriciansguide.co.uk/"]

# Define keywords to search for
keywords = ["electrical theory", "uk electrician", "bs7671", "iet"]


class TextParser(BeautifulSoup):
    def __init__(self, markup="", parser=None, **kwargs):
        super().__init__(markup, parser, **kwargs)


    # Override the get_text method to exclude certain tags
    def get_text(self, *args, **kwargs):
        kwargs['separator'] = ' '
        kwargs['strip'] = True
        return super().get_text(*args, **kwargs)

    # Check if the page matches the search criteria
    def check_page(self, content):
        for keyword in keywords:
            if keyword not in content.lower():
                return False
        return True

    # Get the hyperlinks from a URL that are within the same domain and match the search criteria
    def get_domain_hyperlinks(self, local_domain: str, url: str) -> List[str]:
        clean_links = []
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        text = soup.get_text()

        if self.check_page(text):
            # Save the text to a txt file if the page matches the search criteria
            with open(f'text/{local_domain}/{url[8:].replace("/", "_")}.txt', "w") as f:
                f.write(text)

            # Get the hyperlinks from the URL that are within the same domain and match the search criteria
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None:
                    if re.search(HTTP_URL_PATTERN, href):
                        url_obj = urllib.parse.urlparse(href)
                        if url_obj.netloc == local_domain:
                            clean_links.append(href)
                    else:
                        clean_link = urllib.parse.urljoin(url, href).split("#")[0]  # Remove anchor links
                        if clean_link.startswith(f"https://{local_domain}") or clean_link.startswith(
                                f"http://{local_domain}"):
                            clean_links.append(clean_link)

        return list(set(clean_links))

    def crawl(self, url, depth=0):
        text = requests.get(url).text
        soup = TextParser(text, "html.parser").soup

    
        # Parse the URL and get the domain
        local_domain = urllib.parse.urlparse(url).netloc

        # Create a queue to store the URLs to crawl
        queue = deque([(url, depth)])

        # Create a set to store the URLs that have already been seen (no duplicates)
        seen = set([url])

        # Create a directory to store the text files
        if not os.path.exists("text/"):
                os.mkdir("text/")

        if not os.path.exists("text/" + local_domain + "/"):
                os.mkdir("text/" + local_domain + "/")

        # While the queue is not empty, continue crawling
        while queue:
            # Get the next URL and depth from the queue
            url, depth = queue.pop()
            logging.info(f"URL: {url}, Depth: {depth}")

            # If the depth limit has been reached, continue with the next URL
            if depth >= MAX_DEPTH:
                continue

            # Get the hyperlinks from the URL that are within the same domain and match the search criteria
            for link in self.get_domain_hyperlinks(local_domain, url):
                if link not in seen:
                    queue.append((link, depth + 1))
                    seen.add(link)

            # Write the text to a file if the page matches the search criteria
            soup = TextParser(requests.get(url).text, "html.parser")
            text = soup.get_text()
            if self.check_page(text):
                with open(f'text/{local_domain}/{url[8:].replace("/", "_")}.txt', "w") as f:
                    f.write(text)
                    logging.info(f"Saved text to file: text/{local_domain}/{url[8:].replace('/', '_')}.txt")


TextParser().crawl("https://www.electricalsafetyfirst.org.uk/", depth=0)
