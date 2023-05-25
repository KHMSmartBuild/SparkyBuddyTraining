# Script name : selenium_web_scraping.py
# location : agents\safety_agents\selenium_web_scraping.py
# accessible from Libraries = Libraries not initialized yet #TODO Create Libraries Structure
# Author: KHM Smartbuild
# Created: 24/05/2023   
# Updated: 24/05/2023
# Copyright: (c) 2023 KHM Smartbuild
# Purpose: This script is designed to handle web scraping tasks using Selenium. It includes functions for browsing websites, 
# scraping text and links from websites, and managing the Selenium WebDriver.

from __future__ import annotations

from selenium import webdriver
from sparky_buddy.processing.html import extract_hyperlinks, format_hyperlinks
import sparky_buddy.processing.text as summary
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
import logging
from pathlib import Path
from sparky_buddy.config import Config

FILE_DIR = Path(__file__).parent.parent
CFG = Config()

# The rest of the script remains the same...
