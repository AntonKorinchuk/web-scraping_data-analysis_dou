# Web Scraping and Data Analysis from DOU

This project scrapes job vacancy data from jobs.dou.ua and performs data analysis to gain insights into job vacancies,
experience levels, salary ranges, and popular technologies.

Project focuses on collecting and analyzing job vacancy data for Python developers from the jobs.dou.ua website. Using a
Scrapy spider, Selenium for dynamic content, and Pandas/Numpy for data processing, we extract information such as job
titles, companies, salaries, required technologies, and experience levels. Data visualizations are then generated to
highlight key trends in the job market.

# Technologies
### The following libraries and frameworks are used in this project:

- Scrapy - for web scraping
- Selenium - for handling dynamically loaded content
- Pandas - for data manipulation and analysis
- Numpy - for numerical operations
- Matplotlib - for data visualization

# Installing using GitHub
Follow these steps to set up the project locally:


Clone the repository and switch to the project directory:
```shell
git https://github.com/AntonKorinchuk/web-scraping_data-analysis_dou.git
cd web-scraping_data-analysis_dou
```

Create a virtual environment:
```shell
python -m venv venv
```

Activate the virtual environment:
On Windows:
```shell
 venv\Scripts\activate
 ```
On macOS and Linux:
```shell
source venv/bin/activate
```

Install dependencies:
```shell
pip install -r requirements.txt
```

To start scraping, run the Scrapy spider:
```shell
scrapy crawl vacancies -O vacancies.csv
```

Run the notebook:
```shell
jupyter notebook
```

# Data Analysis
### The analysis includes:

- Vacancies by Experience Level:
Visualized using a pie chart.
Data stored in [vacancies_by_experience.png](data/vacancies_by_experience.png)

- Salary by Experience Level:
Bar chart comparing the average minimum and maximum salaries for Junior, Middle, and Senior levels.
Data stored in [salary_by_experience.png](data/salary_by_experience.png)

- Most Popular Technologies:
Bar chart showing the most frequently mentioned technologies in job descriptions.
Data stored in [most_popular_technologies.png](data/most_popular_technologies.png)

