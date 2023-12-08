class JobExtractor:

    def __init__(self, job):
        self.job = job

    def get_job_title(self):
        return self.job.find('h3', class_='base-search-card__title').text.strip()

    def get_job_company(self):
        return self.job.find('h4', class_='base-search-card__subtitle').text.strip()

    def get_job_location(self):
        return self.job.find('span', class_='job-search-card__location').text.strip()

    def get_job_datetime(self):
        datetime_obj = self.job.find('time', class_='job-search-card__listdate')
        if datetime_obj is None:
            datetime_obj = self.job.find('time', class_='job-search-card__listdate--new')
        return datetime_obj['datetime']

    def get_job_salary(self):
        salary_obj = self.job.find('span', class_='job-search-card__salary-info')
        return salary_obj.text.strip() if salary_obj is not None else "NaN"

    def get_job_link(self):
        return self.job.find('a', class_='base-card__full-link')['href']

    def get_job_criteria(self):
        return [
            self.get_job_title(),
            self.get_job_company(),
            self.get_job_location(),
            self.get_job_datetime(),
            self.get_job_salary(),
            self.get_job_link(),
        ]