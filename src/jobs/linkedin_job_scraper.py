from bs4 import BeautifulSoup
import requests

from src.entity.linkedin_job_extractor import JobExtractor


class LinkedinJobScraper:

    def __init__(self, job, count, country, onsite_remote, response):
        self.job_extractor = JobExtractor(job)
        self.count = count
        self.country = country
        self.onsite_remote = onsite_remote
        self.response = response
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def scrape_linkedin_job_details(self):
        job_criteria = self.job_extractor.get_job_criteria()

        while True:
            try:
                resp = requests.get(self.job_extractor.get_job_link(), headers=self.headers)
                print('Scraping job details...')
            except:
                print("Connection refused by the server during the scrap..")
                continue

            sp = BeautifulSoup(resp.content, 'html.parser')
            # Save requests as html pages to help view classes for scraping
            if self.count == 0 and self.country == 'africa':
                with open('../scrap_page_view/job-list.html', mode='w', encoding="utf-8") as job_list:
                    job_list.write(str(self.response.content))
                    job_list.close()
                with open('../scrap_page_view/job.html', mode='w', encoding="utf-8") as job_detail:
                    job_detail.write(str(resp.content))
                    job_detail.close()
            self.count += 1

            job_desc = sp.find('div',
                               class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5').text.strip(
            ) if sp.find('div',
                         class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5') is not None else "Nan"

            criteria = sp.find_all('li', class_='description__job-criteria-item')
            for criterion in criteria:
                feature = criterion.find('h3', class_='description__job-criteria-subheader').text.strip()
                value = criterion.find('span',
                                       class_='description__job-criteria-text '
                                              'description__job-criteria-text--criteria').text.strip()
                job_criteria.append({feature: value})

            job_data = [
                self.job_extractor.get_job_title(), self.job_extractor.get_job_company(), job_desc,
                self.onsite_remote, self.job_extractor.get_job_salary(), self.job_extractor.get_job_location(),
                job_criteria, self.job_extractor.get_job_datetime(), self.job_extractor.get_job_link()
            ]

            print('Data updated')
            return job_data

    def linkedin_scraper(self, webpage, page_number, onsite_remote, country_link):
        count = 0
        next_page = webpage + str(page_number)
        response = requests.get(str(next_page), headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = soup.find_all(
            'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link '
                          'base-search-card base-search-card--link job-search-card')
        for job in jobs:
            job_scraper = LinkedinJobScraper(job, count, country_link, onsite_remote, response, headers=self.headers)
            job_scraper.scrape_linkedin_job_details()

        if page_number < 500:
            page_number = page_number + 25
            self.linkedin_scraper(webpage, page_number, onsite_remote)
