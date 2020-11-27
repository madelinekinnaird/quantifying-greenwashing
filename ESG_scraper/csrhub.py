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
url = 'https://www.csrhub.com/'

output_path = pathlib.Path('../data/')


ESG_file = output_path.joinpath("ESG.csv").open("w")
ESG_writer = csv.DictWriter(ESG_file, fieldnames=["company", "overall", "energy_rating", "environment_rating", "resource_rating"])

ESG_writer.writeheader()


companies = open("batch.txt", "r")
## open driver
driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
wait = WebDriverWait(driver, 10)


## go to URL
driver.get(url)


#
▼



## login
driver.find_element_by_xpath('//*[@id="additional-menu"]/ul/li/a').click()
login = driver.find_element_by_id('inputUsername')
login.send_keys('EMAIL HERE')
password = driver.find_element_by_id('inputPassword')
password.send_keys('PASSWORD HERE')
sign_in = driver.find_element_by_xpath('//*[@id="modal-signin"]/div/div/div[3]/button[2]').click()


## loop through companies
for company_to_search in companies:


    time.sleep(1)

    ## go to URL
    driver.get(url)

    time.sleep(2)
    ## navigate to company page
    driver.find_element_by_xpath('//*[@id="select2-lookup-string-min-container"]/span').click()
    search = driver.find_element_by_css_selector('body > span > span > span.select2-search.select2-search--dropdown > input')

    ## sleep
    time.sleep(1)

    search.send_keys(company_to_search)
    #option = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[.='%s']" % company_to_search)))
    time.sleep(1)

    search.send_keys(Keys.ENTER)

    ## wait for page to load
    time.sleep(15)
    #<a class="company-profile__ranking-sheet_name-link company-profile__ranking-sheet_name-link_default">Dick's Sporting Goods, Inc.<i class="">▼</i></a>
        # Execute script to scroll down the page and make sure that we are loading the full page
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
    # Sleep for 3 seconds to load whole page
    time.sleep(1)

    ## get page RESOURCE
    html_source = driver.page_source

    type(html_source)
    want to find the word "The Board"
    The next instance of <span class="value">
    save the two characters after









    ## locate table
    #rating-section > div > div.company-profile__section_content > div > div > table
    driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(15)').click()

    ## click tab expansion
    driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(15)').click()
    driver.find_element(By.CSS_SELECTOR("#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(14) > td:nth-child(1) > a > i")).Click();
    ## OVERALL CLIMATE RATING
    overall_class = driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(22) > td:nth-child(5) > div > div > span > span')
    overall = overall_class.text


    ## ENERGY AND CLIMATE RATING
    energy_class = driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(23) > td:nth-child(5) > div > table > tbody > tr > td:nth-child(2) > div > div > span.pp.pp43 > span')
    energy = energy_class.text


    ## ENVIRONMENT POLICY AND REPORTING
    environment_class = driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(24) > td:nth-child(5) > div > table > tbody > tr > td:nth-child(2) > div > div > span.pp.pp43 > span')
    environment = environment_class.text


    ## RESOURCE MANAGEMENT
    resource_class = driver.find_element_by_css_selector('#rating-section > div > div.company-profile__section_content > div > div > table > tbody > tr:nth-child(25) > td:nth-child(5) > div > table > tbody > tr > td:nth-child(2) > div > div > span.pp.pp43 > span')
    resource = resource_class.text


    company_data = {'company': company_to_search,'overall': overall, 'energy_rating': energy,'environment_rating': energy,'resource_rating': resource}


    ESG_writer.writerow(company_data)



#user_file.close()
ESG_file.close()

## table
//*[@id="rating-section"]/div/div[2]/div/div/table


company_data = {'company': company,'overall': overall_environment, 'energy_rating': energy,'environment_rating': energy,'resource_rating': resource}

company_data = {'company': 'Tesla Motors, Inc.','overall_environment': 51, 'energy_rating': 57,'environment_rating': 47,'resource_rating': 51}

## energy climate rating
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[15]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 4 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[19]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 5 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[23]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 6 columns

## environment rating
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[16]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 4 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[20]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 5 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[24]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 6 columns

## resource rating
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[17]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 4 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[21]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 5 columns
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[25]/td[5]/div/table/tbody/tr/td[2]/div/div/span[1]/span ## 6 columns



company_data'
## 1,1
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[14]/td[1]/a
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[18]/td[1]/a


## 2,1
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[14]/td[2]/div/span[1]/span
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[18]/td[2]/div/span[1]/span

## 2,2
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[18]/td[2]/div/span/span
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[22]/td[2]/div/span/span

## 2,3
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[22]/td[2]/div/span/span
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[26]/td[2]/div/span/span
## 2,4
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[26]/td[2]/div/span/span
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[30]/td[2]/div/span/span
## 2,5
----
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[34]/td[2]/div/span/span


## 3,1
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[14]/td[3]/div/div/span/span
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[18]/td[3]/div/div/span/span

## 3,2
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[18]/td[3]/div/div/span/span

## 3,3
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[22]/td[3]/div/div/span/span

## 3,4
//*[@id="rating-section"]/div/div[2]/div/div/table/tbody/tr[26]/td[3]/div/div/span/span
