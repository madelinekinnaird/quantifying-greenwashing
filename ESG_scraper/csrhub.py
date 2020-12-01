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

## CSV prep
output_path = pathlib.Path('../data/')
ESG_file = output_path.joinpath("ESG.csv").open("w")
ESG_writer = csv.DictWriter(ESG_file, fieldnames=['company', 'overall','community', 'employees', 'environment', 'governance','community_dev','compensation','energy','board','product','diversity','environment','leadership','human_rights', 'training','resource', 'transparency'])
ESG_writer.writeheader()


def csr_scraper(span):
    '''
    function to specify ESG scores
    '''
    for i in range(0,len(span)):
        content = span[i].text
        ## select only the numeric values
        if len(content) == 2 and content != '\n\n':
            print(content)
            ratings.append(content)

        company = company_to_search
        overall = ratings[-17]
        community= ratings[-16]
        employees= ratings[-15]
        environment= ratings[-14]
        governance= ratings[-13]
        community_dev= ratings[-12]
        compensation = ratings[-11]
        energy= ratings[-10]
        board = ratings[-9]
        product= ratings[-8]
        diversity = ratings[-7]
        environment = ratings[-6]
        leadership = ratings[-5]
        human_rights = ratings[-4]
        training = ratings[-3]
        resource= ratings[-2]
        transparency = ratings [-1]

        return [company,overall,community,employees,environment,governance,community_dev,compensation,energy,board,product,diversity,environment,leadership,human_rights,training,resource,transparency]


## get list of companies
companies = open("batch.txt", "r")


## open driver
driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
wait = WebDriverWait(driver, 10)
url = 'https://www.csrhub.com/'


## login
driver.get(url)
driver.find_element_by_xpath('//*[@id="additional-menu"]/ul/li/a').click()
login = drivmadedliner.find_element_by_id('inputUsername')
login.send_keysmk208('EMAIL HERE')
password = driver.find_element_by_id('inputPassword')
password.send_keys('PASSWORD HERE')
sign_in = driver.find_element_by_xpath('//*[@id="modal-signin"]/div/div/div[3]/button[2]').click()


scraped_data = []


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

    ## get page html
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    span = soup.select('span',{'class':'value'})

    rating = []

    ## append to scraped data list
    scraped_data.append(csr_scraper(span))


scraped_data

## turn list to dataframe then to CSV
data = pd.DataFrame(scraped_data,columns=['company', 'overall','community', 'employees', 'environment', 'governance','community_dev','compensation','energy','board','product','diversity','environment','leadership','human_rights', 'training','resource', 'transparency'])
data.to_csv("esg_ratings.csv",index=False)
