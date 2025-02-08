import requests
import json
from bs4 import BeautifulSoup
import time

num_pages = 900

id_list = []
for page in range(num_pages):
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start={page}"
    response = requests.get(list_url)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")

    for job in page_jobs:
        try:
            base_card_div = job.find("div", {"class": "base-card"})
            if base_card_div:
                job_id = base_card_div.get("data-entity-urn").split(":")[3]
                id_list.append(job_id)
        except:
            print(f"Skipping {page} due to error")
    time.sleep(2)
    


with open("job_ids.json", "w") as file:
    json.dump(id_list, file)

job_list = []
count = 0
with open("job_ids.json", "r") as file:
    job_ids = json.load(file)
    for job_id in job_ids:
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        job_response = requests.get(job_url)
        job_soup = BeautifulSoup(job_response.text, "html.parser")
        
        job_post = {}

        try:
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
        except:
            job_post["job_title"] = None
        
        try:
            job_description_section = job_soup.select_one("div.description__text--rich .show-more-less-html__markup")
            job_post["job_description"] = job_description_section.get_text(separator="\n", strip=True)
        except:
            job_post["job_description"] = None

        try:
            criteria_items = job_soup.select("ul.description__job-criteria-list li.description__job-criteria-item")
            job_post["seniority_level"] = criteria_items[0].select_one("span.description__job-criteria-text").get_text(strip=True)
        except:
            job_post["seniority_level"] = None
        
        try:
            criteria_items = job_soup.select("ul.description__job-criteria-list li.description__job-criteria-item")
            job_post["employment_type"] = criteria_items[1].select_one("span.description__job-criteria-text").get_text(strip=True)
        except:
            job_post["employment_type"] = None

        try:
            job_post["salary"] = job_soup.find("div", {"class":"salary compensation__salary"}).text.strip()
        except:
            job_post["salary"] = None

        try:
            job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
        except:
            job_post["company_name"] = None
        
        try:
            job_post["location"] = job_soup.select_one("span.topcard__flavor--bullet").get_text(strip=True)
        except:
            job_post["location"] = None

        try:
            job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata"}).text.strip()
        except:
            job_post["time_posted"] = None
            
        try:
            job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption"}).text.strip()
        except:
            job_post["num_applicants"] = None

        try:
            job_post["job_link"] = job_soup.find("div", class_="top-card-layout__entity-info").find("a", class_="topcard__link")["href"]
        except:
            job_post["job_link"] = None
        
        count += 1
        print(count)
        job_list.append(job_post)
        time.sleep(0.03) 


with open("job_lists.json", "w") as file:
    json.dump(job_list, file, indent=4)
    print("File created successfully")
