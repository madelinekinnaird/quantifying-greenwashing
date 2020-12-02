from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


import pandas as pd
import numpy as np

## import list of fortune 500 companies
data = pd.read_csv('../data/fortune_500_companies.csv')
data[column] = data[column].astype(str)
url = 'https://www.csrhub.com/'

column = 'NAME'
df = data

## remove rows where there isn't a valid instagram
df = df[df.INSTAGRAM != 'x']


f = open("batch.txt","w+")


for row in df[column]:
    ## skip rows with an x
    if row == 'x':
        pass
    else:
        print(row)
        ## open chrome driver
        driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')

        ## go to URL

        driver.get(url)


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

        f.write(proper_name + '\n')
        driver.close()
        time.sleep(3)

f.close()
