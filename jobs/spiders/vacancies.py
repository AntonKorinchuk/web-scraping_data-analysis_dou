from typing import Generator
import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
import time
from collections import Counter
import re


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = [
        "https://jobs.dou.ua/vacancies/?category=Python&exp=0-1",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=1-3",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=3-5",
        "https://jobs.dou.ua/vacancies/?category=Python&exp=5plus",
    ]

    technologies = [
        "Python",
        "Django",
        "Flask",
        "FastAPI",
        "Pyramid",
        "Tornado",
        "Bottle",
        "AWS",
        "RoboDK",
        "API",
        "Azure",
        "Google Cloud Platform",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Ansible",
        "Celery",
        "Redis",
        "RabbitMQ",
        "Apache Kafka",
        "PostgreSQL",
        "MySQL",
        "SQLite",
        "MongoDB",
        "Elasticsearch",
        "SQLAlchemy",
        "Peewee",
        "Jenkins",
        "GitLab CI",
        "CircleCI",
        "Travis CI",
        "Sentry",
        "New Relic",
        "Grafana",
        "Prometheus",
        "pytest",
        "unittest",
        "coverage.py",
        "tox",
        "requests",
        "httpx",
        "aiohttp",
        "BeautifulSoup",
        "Scrapy",
        "Pytest-Django",
        "Flask-RESTful",
        "DRF",
        "Pydantic",
        "Marshmallow",
        "OpenCV",
        "TensorFlow",
        "PyTorch",
        "scikit-learn",
        "Keras",
        "NLTK",
        "spaCy",
        "Jupyter",
        "Matplotlib",
        "Seaborn",
        "Plotly",
        "Dash",
        "Pygame",
        "Pandas",
        "NumPy",
        "SciPy",
        "SymPy",
        "ML",
        "GIT"
    ]

    experience_levels = {
        "0-1": "junior",
        "1-3": "middle",
        "3-5": "senior",
        "5plus": "senior",
    }

    tech_counter = Counter()

    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def parse(
        self, response: Response, **kwargs
    ) -> Generator[scrapy.Request, None, None]:
        self.driver.get(response.url)

        while True:
            try:
                load_more_button = self.driver.find_element(
                    "css selector", ".more-btn a"
                )
                load_more_button.click()
                time.sleep(2)
            except Exception:
                break

        sel = Selector(text=self.driver.page_source)

        for job in sel.css("li.l-vacancy"):
            job_url = job.css("a.vt::attr(href)").get()
            yield response.follow(
                job_url, callback=self.parse_job, meta={"start_url": response.url}
            )

    def parse_job(self, response: Response) -> Generator[dict, None, None]:
        title = response.css("h1.g-h2::text").get()
        company = response.css("div.l-n a::text").get()
        job_description = " ".join(
            response.css("div.b-typo.vacancy-section *::text").getall()
        )
        job_link = response.url

        start_url = response.meta.get("start_url", "")
        techs_in_job = self.extract_technologies(job_description)
        experience_level = self.extract_experience_level(start_url)

        self.tech_counter.update(techs_in_job)

        yield {
            "title": title,
            "company": company,
            "technologies": techs_in_job,
            "experience_level": experience_level,
            "link": job_link,
        }

    def extract_technologies(self, job_description: str) -> list:
        found_technologies = []
        for tech in self.technologies:
            if tech.lower() in job_description.lower():
                found_technologies.append(tech)
        return found_technologies

    def extract_experience_level(self, url: str) -> str:
        exp_match = re.search(r"exp=(\d+-\d+|5plus)", url)
        if exp_match:
            exp = exp_match.group(1)
            return self.experience_levels.get(exp, "unknown")
        return "unknown"

    def closed(self, reason):
        print("The most popular technologies:")
        for tech, count in self.tech_counter.most_common():
            print(f"{tech}: {count} times")

        self.driver.quit()
