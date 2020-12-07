from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pathlib
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os



## get list of companies
cdf = pd.read_csv('../../../data/company_key.csv')
column = 'company'
companies = df[column]


## open driver
driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
wait = WebDriverWait(driver, 10)
url = 'https://www.csrhub.com/'



## login
driver.get(url)
driver.fimk2080nd_element_by_xpath('//*[@id="additional-menu"]/ul/li/a').click()
login = drivmadedliner.find_element_by_id('inputUsername')
login.send_keys('EMAIL HERE')
password = driver.find_element_by_id('inputPassword')
password.send_keys('PASSWORD HERE')
sign_in = driver.find_element_by_xpath('//*[@id="modal-signin"]/div/div/div[3]/button[2]').click()


## dictionary for scraped data
scraped_data = {}



## loop through companies
for company_to_search in companies:
    ## set new ratings list
    ratings = []

    ## go to URL
    driver.get(url)

    time.sleep(2)

    ## navigate to company page
    driver.find_element_by_xpath('//*[@id="select2-lookup-string-min-container"]/span').click()
    search = driver.find_element_by_css_selector('body > span > span > span.select2-search.select2-search--dropdown > input')
    time.sleep(1)
    search.send_keys(company_to_search)
    time.sleep(1)
    search.send_keys(Keys.ENTER)

    ## wait for page to load
    time.sleep(15)

    ## get page html
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    all_span = soup.select('span')

    ## find just the number ratings on the page
    for span in all_span:
        content = span.text
        if len(content) == 2 and content != '\n\n':
            ratings.append(content)

    company = company_to_search
    overall_rating = ratings[0]
    community_rating = ratings[1]
    employee_rating = ratings[2]
    environment_rating = ratings[3]
    governance_rating = ratings[4]
    overall_percentage = ratings[5]
    community_percentage = ratings[7]
    employee_percentage = ratings[9]
    environment_percentage = ratings[11]
    governance_percentage = ratings[13]

    ratingsList = [company, overall_rating, community_rating, employee_rating, environment_rating, governance_rating, overall_percentage, community_percentage, employee_percentage, environment_percentage, governance_percentage]
    scraped_data[company] = ratingsList

## check to see if our scraper worked!
scraped_data

## turn into dataframe
df = pd.DataFrame.from_dict(scraped_data, orient='index', columns = cols)
df.reset_index(drop=True, inplace=True)
df

## export to CSV
path = '../../../data'
df.to_csv(os.path.join(path,r'esg_ratings.csv'))
