## driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

## data manipulation
import pandas as pd
import numpy as np


## import company key and set column
df = pd.read_csv('../../../data/company_key.csv')
column = 'company'
companies = df[column]

## url to search on
url = 'https://www.csrhub.com/'

## start driver
driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')

## list to store proper names
esg_company = []



for row in companies:
    ## go to URL
    driver.get(url)

    ## click on search feature
    search_click = driver.find_element_by_xpath('//*[@id="select2-lookup-string-min-container"]/span').click()
    time.sleep(1)
    search = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
    time.sleep(1)
    search.send_keys(row)

    ## search for proper name
    lookup = driver.find_element_by_xpath('//*[@id="select2-lookup-string-min-results"]')
    time.sleep(2)
    proper_name = lookup.text
    proper_name = proper_name.split('\n')[0]


    print(proper_name)
    esg_company.append(proper_name)


## input updated list into df column
df['esg_company'] = esg_company

## update current csv
path = '../../../data'
df.to_csv(os.path.join(path,r'company_key.csv'))
