"""
Selenium web scraping module.

# Script name : sparky_browse_webpage.py
# location = gui\Sparky\sparky_browse_webpage.py
# accessible from Libraries = yes
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
# Purpose: Browse a webpage and summarize it using the LLM model

"""

"""
Browse a webpage and summarize it using the LLM model
"""
from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


def get_response(url: str, timeout: int = 10) -> tuple[None, str] | tuple[requests.Response, None]:
    """
    Get the response from a URL

    Args:
        url (str): The URL to get the response from
        timeout (int): The timeout for the HTTP request

    Returns:
        tuple[None, str] | tuple[Response, None]: The response and error message

    Raises:
        ValueError: If the URL is invalid
        requests.exceptions.RequestException: If the HTTP request fails
    """
    try:
        # Most basic check if the URL is valid:
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL format")

        sanitized_url = urlparse(url)._replace(scheme="https").geturl() # replace http with https
        response = session.get(sanitized_url, timeout=timeout)

        # Check if the response contains an HTTP error
        if response.status_code != 200:
            raise requests.exceptions.RequestException(
                f"HTTP request failed with code {response.status_code}"
            )

        soup = BeautifulSoup(response.text, "html.parser") # create BeautifulSoup instance for parsing HTML
        
        return response, soup

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        return None, error_message
