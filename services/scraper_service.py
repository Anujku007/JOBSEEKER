import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ScraperService:
    """Smart Indian Job Scraper (2025) — smooth fallback"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        ]

    def _headers(self):
        return {"User-Agent": random.choice(self.user_agents)}

    def _driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape_naukri(self, keyword="python", location="Bengaluru", use_selenium=False):
        jobs = []
        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
        try:
            html = None
            if use_selenium:
                driver = self._driver()
                driver.get(url)
                time.sleep(4)
                html = driver.page_source
                driver.quit()
            else:
                r = requests.get(url, headers=self._headers(), timeout=10)
                if r.status_code != 200 or "captcha" in r.text.lower():
                    raise Exception("Blocked - Naukri")
                html = r.text

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select("div.srp-jobtuple-wrapper, div.jobTuple.bgWhite.br4.mb-8")
            for c in cards:
                title = c.select_one("a.title")
                company = c.select_one("a.comp-name, a.subTitle")
                if not title or not company:
                    continue
                jobs.append({
                    "id": f"naukri_{random.randint(1000,9999)}",
                    "title": title.text.strip(),
                    "company": company.text.strip(),
                    "location": location,
                    "salary": "Not Disclosed",
                    "description": "Job listing from Naukri India",
                    "url": title.get("href", "#"),
                    "posted_date": datetime.now().strftime("%b %d, %Y"),
                    "remote": "remote" in title.text.lower(),
                    "source": "Naukri"
                })

            if not jobs and not use_selenium:
                self.logger.warning("⚠️ Naukri returned 0 jobs, retrying with Selenium")
                return self.scrape_naukri(keyword, location, use_selenium=True)
        except Exception as e:
            self.logger.warning(f"❌ Naukri scrape failed: {e}")
        return jobs

    def scrape_indeed(self, keyword="python", location="Bengaluru", use_selenium=False):
        jobs = []
        url = f"https://in.indeed.com/jobs?q={keyword}&l={location}"
        try:
            html = None
            if use_selenium:
                driver = self._driver()
                driver.get(url)
                time.sleep(5)
                html = driver.page_source
                driver.quit()
            else:
                r = requests.get(url, headers=self._headers(), timeout=10)
                if r.status_code != 200 or "captcha" in r.text.lower():
                    raise Exception("Blocked - Indeed")
                html = r.text

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select("div.job_seen_beacon")
            for c in cards:
                title = c.select_one("h2.jobTitle span")
                company = c.select_one("span[data-testid='company-name']")
                if not title or not company:
                    continue
                jobs.append({
                    "id": f"indeed_{random.randint(1000,9999)}",
                    "title": title.text.strip(),
                    "company": company.text.strip(),
                    "location": location,
                    "salary": "Not Disclosed",
                    "description": "Job listing from Indeed India",
                    "url": "https://in.indeed.com",
                    "posted_date": datetime.now().strftime("%b %d, %Y"),
                    "remote": "remote" in title.text.lower(),
                    "source": "Indeed"
                })

            if not jobs and not use_selenium:
                self.logger.warning("⚠️ Indeed returned 0 jobs, retrying with Selenium")
                return self.scrape_indeed(keyword, location, use_selenium=True)
        except Exception as e:
            self.logger.warning(f"❌ Indeed scrape failed: {e}")
        return jobs

    def get_jobs(self, keyword="python", location="Bengaluru"):
        try:
            self.logger.info(f"🔎 Scraping jobs for {keyword} in {location}")
            naukri = self.scrape_naukri(keyword, location)
            indeed = self.scrape_indeed(keyword, location)
            all_jobs = naukri + indeed
            if not all_jobs:
                self.logger.warning("⚠️ Both scrapers returned no jobs, fallback to empty list")
            # Deduplicate
            seen = set()
            unique = []
            for j in all_jobs:
                key = (j["title"], j["company"])
                if key not in seen:
                    seen.add(key)
                    unique.append(j)
            return unique
        except Exception as e:
            self.logger.error(f"Scraper error: {e}")
            return []
