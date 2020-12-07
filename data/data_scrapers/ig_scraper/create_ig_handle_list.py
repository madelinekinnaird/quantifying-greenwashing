## driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

## data manipulation
import pandas as pd
import numpy as np
import os


## import company key and set column
df = pd.read_csv('../../../data/company_key.csv')
column = 'company'
companies = df[column]



## driver to instagram
url = 'https://www.instagram.com/'
driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
driver.get(url)
## add instagram options for login

## list to store proper names
verified_list = []
username_list = []
completed_companies = []


for company in companies:
    if company in completed_companies:
        print("Already checked", company)
        continue
    print("Checking", company, "...")

    ## go to URL
    driver.get(url)

    ## click on search feature
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div/div/span[2]').click()
    ## clear previous search
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]').click()
    # search for company
    search = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    time.sleep(1)
    search.send_keys(company)
    time.sleep(2.5)

    ## retrieve info from the first drop down
    try:
        lookup = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]')

        user = lookup.text
        user_info = user.split('\n')
        if len(user_info) < 2:
            username_list.append("Not Verified")
            verified_list.append("Not Verified")
            completed_companies.append(company)

        else:
            handle = user_info[0]
            verified = user_info[1]

            username_list.append(handle)
            verified_list.append(verified)
            completed_companies.append(company)

    except NoSuchElementException:
        print("Nothing found!")
        username_list.append("Not Found")
        verified_list.append("Not Found")
        completed_companies.append(company)
        pass



## input updated list into df column
df['username'] = username_list
df['verified'] = verified_list



## update current csv
path = '../../../data'
df.to_csv(os.path.join(path,r'company_key1.csv'))
