# Python webscraper using Selenium 
# Scrape Job openings from Linkedin and store in csv 
# Author: Vivek Udupa
# Start Date: June 22, 2021

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import re

from bs4 import BeautifulSoup as bsp
from bs4 import NavigableString
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
scroll_num = 5
x = 1

body = driver.find_element_by_css_selector('body')
body.click()
while (x < scroll_num):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    print("scroll ", x)
    x = x + 1
# getting the number of jobs listed in the webpage
pageSource = driver.page_source
lxml_soup = bsp(pageSource, 'lxml')

job_list = lxml_soup.find('ul', class_ = 'jobs-search__results-list')

print(f'Collecting info about {len(job_list)} jobs')

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
    job_description.append("-----New Job-----")

