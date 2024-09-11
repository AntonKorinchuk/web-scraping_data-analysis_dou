from typing import Generator
import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.selector import Selector
import time
from collections import Counter
import re

from config import TECHNOLOGIES, EXPERIENCE_LEVELS, URLS


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = URLS
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
        salary = (
            response.css("div.sh-info span.salary::text")
            .get(default="Not specified")
            .strip()
        )
        salary = self.clean_salary(salary)

        start_url = response.meta.get("start_url", "")
        techs_in_job = self.extract_technologies(job_description)
        experience_level = self.extract_experience_level(start_url)

        self.tech_counter.update(techs_in_job)

        yield {
            "title": title,
            "company": company,
            "salary_in_$": salary,
            "technologies": techs_in_job,
            "experience_level": experience_level,
            "link": job_link,
        }

    def extract_technologies(self, job_description: str) -> list:
        found_technologies = []
        for tech in TECHNOLOGIES:
            if tech.lower() in job_description.lower():
                found_technologies.append(tech)
        return found_technologies

    def extract_experience_level(self, url: str) -> str:
        exp_match = re.search(r"exp=(\d+-\d+|5plus)", url)
        if exp_match:
            exp = exp_match.group(1)
            return EXPERIENCE_LEVELS.get(exp, "unknown")
        return "unknown"

    def clean_salary(self, salary: str) -> str:
        salary = (
            salary.lower()
            .replace("від", "")
            .replace("дол.", "")
            .replace("$", "")
            .strip()
        )
        salary_match = re.search(r"(\d+)\s*[-–]\s*(\d+)", salary)

        if salary_match:
            min_salary = int(salary_match.group(1))
            max_salary = int(salary_match.group(2))
            return f"{min_salary}-{max_salary}"

        single_salary_match = re.search(r"(\d+)", salary)
        if single_salary_match:
            return f"{single_salary_match.group(1)}-{single_salary_match.group(1)}"

        return "Not specified"

    def closed(self, reason):
        print("The most popular technologies:")
        for tech, count in self.tech_counter.most_common():
            print(f"{tech}: {count} times")

        self.driver.quit()
