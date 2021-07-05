# Python webscraper using Selenium 
# Scrape Job openings from Linkedin and store in csv 
# Author: Vivek Udupa
# Start Date: June 22, 2021

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import re

from bs4 import BeautifulSoup as bsp
from bs4 import NavigableString

import pandas as pd
# Set path to chromedriver
PATH_new = "/home/vivek/Codelab/JobHunt/PythonDataScraper/Chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=PATH_new)
driver.maximize_window()

# Initialize link to website that is to be scraped

#website = "https://www.linkedin.com/jobs"

website = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&sortBy=R&f_TPR=&f_E=2&f_JT=F&position=1&pageNum=0"
driver.get(website)
time.sleep(2)

#Scroll down to load more job listings
num_jobs = 6

# getting the number of jobs listed in the webpage


# Scroll to find more jobs
job_list = []
num_jobs_found = 0
delay = 100 #seconds
while(num_jobs_found < num_jobs):
       
    pageSource = driver.page_source
    lxml_soup = bsp(pageSource, 'lxml')
    
    job_list.clear()   
    job_list = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
    
    num_jobs_found = int(len(job_list)/4)
    print(f'Collecting info about {num_jobs_found} jobs')
    
    try:
        button_moreJobs = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Load more results']")))
        button_moreJobs.click()
        time.sleep(3)
    except:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        continue


# initializing parameters for scraping 

job_id = [] # unique job id
job_title = [] # posted job title
job_company = [] # company name 
job_date = [] # posted date
job_loc = [] # job location
job_description = [] # job description 
job_level = [] # Experience level
job_type = [] # Employer type
job_functions = [] # job roles / expectations
job_industries = [] # job domain

# Scraping level 1 info

# JOB id, title, company, location and date posted
for job in job_list:
   
    # job title
    
    # Ignore the items with type NAvigableString as they 
    # cannot handle .find() with keyword argument
    if isinstance(job, NavigableString):
        continue
    else:
        titles = job.find("span", class_="screen-reader-text").text
        job_title.append(titles)
    
    # job ID
    ids = job.find('a', href=True)['href']
    ids = re.findall(r'(?!-)([0-9]*)(?=\?)', ids)[0]
    job_id.append(ids)

    # company name
    names = job.find("h4", class_="base-search-card__subtitle").text
    job_company.append(names)

    # Job Location
    locations = job.find("span", class_="job-search-card__location").text
    job_loc.append(locations)

    # posting date
    pDate = job.select_one('time')['datetime']
    job_date.append(pDate)
# Scraping job description and qualifications 
for j_id in range(1,len(job_id)+1):
#for j_id in range(1,6):
    print(f'scrapping {j_id} / {len(job_id)}')
    
    # Click on individual job listing 
    job_xpath = '/html/body/div[1]/div/main/section[2]/ul/li[{}]'.format(j_id)
    driver.find_element_by_xpath(job_xpath).click()
    time.sleep(3)

    # click "show more" 
    driver.find_element_by_xpath("//button[contains(text(),'Show more')]").click()
    time.sleep(3)

    # scrape job description
    jobdesc_xpath = "//div[@class='show-more-less-html__markup']"
    descs = driver.find_element_by_xpath(jobdesc_xpath).text
    job_description.append(descs)

# Close the webpage
driver.close()

# Check list sizes

print("job ID: ", len(job_id))
print("Title: ", len(job_title))
print("Company Name: ", len(job_company))
print("Location: " ,len(job_loc))
print("Posting Date: ", len(job_date))
print("Description: ", len(job_description))

# Creating Pandas DataFrame
job_data = pd.DataFrame({'Job ID' : job_id,
'Title' : job_title,
'Company Name' : job_company,
'Location' : job_loc,
'Posting Date' : job_date,
'Description' : job_description
})

# Cleaning Job Description
job_data['Description'] = job_data['Description'].str.replace('\n', ' ')
job_data['Title'] = job_data['Title'].str.replace('\n', '')
job_data['Company Name'] = job_data['Company Name'].str.replace('\n', '')
job_data['Location'] = job_data['Location'].str.replace('\n', '')
print(job_data.head())

job_data.to_csv('LinkedIn_Job_Data.csv', index=0)
