import csv
import random
import time

import requests
from bs4 import BeautifulSoup

links = {
    # "usa": {
    #     "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3351674810&f_WT=1&geoId=103644278&keywords=data"
    #               "%20analyst&location=United%20States&refresh=true&start=",
    #     "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3205250146&f_WRA=true&f_WT=2&geoId=103644278"
    #               "&keywords=data%20analyst&location=United%20States&refresh=true&start=",
    #     "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3343518868&f_WRA=true&f_WT=3&geoId=103644278"
    #               "&keywords=data%20analyst&location=United%20States&refresh=true&start="},
    #
    # "africa": {
    #     "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3364254624&f_WT=1&geoId=103537801&keywords"
    #               "=data%20analyst&location=Africa&refresh=true&start=",
    #     "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3357561865&f_WT=2&geoId=103537801&keywords"
    #               "=data%20analyst&location=Africa&refresh=true&start=",
    #     "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3363788623&f_WT=3&geoId=103537801&keywords"
    #               "=data%20analyst&location=Africa&refresh=true&start="},

    "canada": {
        # "onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3223346796&f_WT=1&geoId=101174742&keywords"
        #           "=data%20analyst&location=Canada&refresh=true&start=",
        # "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3335356174&f_WT=3&geoId=101174742&keywords"
        #           "=data%20analyst&location=Canada&refresh=true&start=",
        "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3335580667&f_WT=2&geoId=101174742&keywords"
                  "=data%20analyst&location=Canada&refresh=true&start="
    }
}


def fetch_page_content(url, max_retries=5):
    """Fetch and return page content for a given URL, with retries and delays."""
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            wait = 2 ** retries  # Exponential backoff
            print(f"Error fetching URL {url}: {e}. Retrying in {wait} seconds.")
            time.sleep(wait + random.uniform(0, 1))  # Adding randomness to the wait time
            retries += 1
    print(f"Failed to fetch {url} after {max_retries} retries.")
    return None


def parse_job_listing(job):
    """Parse and return job listing details."""
    try:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()

        job_datetime = job.find('time', class_='job-search-card__listdate')
        job_datetime = job_datetime['datetime'] if job_datetime else 'Unknown'

        job_salary = job.find('span', class_='job-search-card__salary-info')
        job_salary = job_salary.text.strip() if job_salary else 'N/A'

        job_link = job.find('a', class_='base-card__full-link')['href']

        # Fetching job description and criteria from the job detail page
        job_detail_content = fetch_page_content(job_link)
        if job_detail_content:
            soup_detail = BeautifulSoup(job_detail_content, 'html.parser')
            job_desc = soup_detail.find('div', class_='show-more-less-html__markup')
            job_desc = job_desc.text.strip() if job_desc else 'N/A'

            criteria_elements = soup_detail.find_all('li', class_='description__job-criteria-item')
            job_criteria = []
            for criterion in criteria_elements:
                feature = criterion.find('h3', class_='description__job-criteria-subheader').text.strip()
                value = criterion.find('span', class_='description__job-criteria-text').text.strip()
                job_criteria.append(f"{feature}: {value}")

            return job_title, job_company, job_desc, job_salary, job_location, job_criteria, job_datetime, job_link

    except Exception as e:
        print(f"Error parsing job listing: {e}")
        return None


def save_page_for_debugging(country, content, file_name):
    """Save HTML content to a file for debugging."""
    if country == 'africa':
        with open(f'scrap_page_view/{file_name}.html', 'w', encoding='utf-8') as file:
            file.write(str(content))


def scrape_jobs(writer, country, webpage, work_type):
    """Scrape job listings and write to CSV."""
    page_number = 0
    while page_number < 500:
        next_page = f"{webpage}{page_number}"
        page_content = fetch_page_content(next_page)

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            jobs = soup.find_all('div', class_='base-card')  # Update class name if necessary

            for job in jobs:
                job_details = parse_job_listing(job)
                if job_details:
                    writer.writerow([*job_details, work_type])

            save_page_for_debugging(country, page_content, 'job-list')
            page_number += 25


def create_job_csv(country_links, country):
    """Create CSV file for job listings of a country."""
    file_path = f'datasets/linkedin-jobs-{country}.csv'
    with open(file_path, mode='w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['title', 'company', 'description', 'work_type', 'salary', 'location', 'criteria', 'posted_date', 'link'])

        for work_type, link in country_links.items():
            scrape_jobs(writer, country, link, work_type)


for country, links in links.items():
    create_job_csv(links, country)
