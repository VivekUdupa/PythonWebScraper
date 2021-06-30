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

# Initialize link to website that is to be scraped

#website = "https://www.linkedin.com/jobs"

website = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=United%20States&locationId=&geoId=103644278&sortBy=R&f_TPR=&f_E=2&f_JT=F&position=1&pageNum=0"
driver.get(website)
time.sleep(2)

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

#print(len(job_title))


#i = job_title[0]

#print(i)
#print ([ord(p) for p in i])

    
    # job ID
    ids = job.find('a', href=True)['href']
    ids = re.findall(r'(?!-)([0-9]*)(?=\?)', ids)[0]
    job_id.append(ids)

    # company name
    names = job.find("h4", class_="base-search-card__subtitle").text
    job_company.append(names)

print(job_company)
print("\n \n \n \n", len(job_company))










# ========================================================= References ====================================
'''
# search and input Job title and desired job location
job_title = "data analyst"
job_location = "United States"

search = driver.find_element_by_name("keywords")
time.sleep(1)
search.send_keys(job_title)

search = driver.find_element_by_name("location")
search.clear()
search.send_keys(job_location)

# Press ENTER
search.send_keys(Keys.RETURN)

time.sleep(2)

# Applying Filter 

# Filter 1: Job Type = Full Time
# Click Job Type drop down filter
button = driver.find_element_by_xpath("//*[contains(text(),'Job Type')]")
button.click()

# Select Full-time option
button = driver.find_element_by_xpath("//*[contains(text(),'Full-time')]")
button.click()

# Click Done
button = driver.find_element_by_xpath("//button[@type ='submit' and (@data-tracking-control-name='public_jobs_f_JT' or @data-tracking-control-name='f_JT-done-btn')]")
button.click()

# Filter 2: Experience Level
button = driver.find_element_by_xpath("//*[contains(text(), 'Experience Level')]")
button.click()

button = driver.find_element_by_xpath("//*[contains(text(), 'Entry level')]")
button.click()

button = driver.find_element_by_xpath("//button[@type ='submit' and (@data-tracking-control-name='public_jobs_f_E' or @data-tracking-control-name='f_E-done-btn')]")
button.click()
'''

'''
attrs = []
for attr in button.get_property('attributes'):
    attrs.append([attr['name'], attr['value']])
print(attrs)
'''


#button = driver.find_element_by_xpath("//label[text()='Full-time']")
#driver.implicitly_wait(10)
#ActionChains(driver).move_to_element(button).click(button).perform()
#time.sleep(2)
#Full-time
#search = driver.find_element_by_id("JOB_TYPE-1")
#search.click()

