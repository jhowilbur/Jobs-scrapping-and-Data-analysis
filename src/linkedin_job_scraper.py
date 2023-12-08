import csv

from src.jobs.linkedin_job_scraper import LinkedinJobScraper

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


def create_job_csv(country_links: dict, country_selected: str):
    all_data = []
    for work_type in country_links:
        job_data = LinkedinJobScraper.linkedin_scraper(country_links[work_type], 0, work_type)
        all_data.extend(job_data)

    with open('datasets/linkedin-jobs-' + country_selected + '.csv', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'company', 'description', 'onsite_remote',
                         'salary', 'location', 'criteria', 'posted_date', 'link'])
        writer.writerows(all_data)


if __name__ == '__main__':
    for country_link in links:
        create_job_csv(links[country_link], country_link)
        # while True:
        #     try:
        #         create_job_csv(links[country_link], country_link)
        #         break
        #     except:
        #         print("Starting again...")
        #         continue
