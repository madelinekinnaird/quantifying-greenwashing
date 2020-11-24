from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pathlib
import csv

url = 'https://www.csrhub.com/'

output_path = pathlib.Path('../data/')


ESG_file = output_path.joinpath("ESG.csv").open("w")
ESG_writer = csv.DictWriter(ESG_file, fieldnames=["company", "energy_rating", "environment_rating", "resource_rating"])

ESG_writer.writeheader()


companies = open("batch.txt", "r")

for company_to_search in companies:
    ## open driver
    driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
    wait = WebDriverWait(driver, 10)

    time.sleep(1)

    ## go to URL
    driver.get(url)

    ## navigate to company page
    search_click = driver.find_element_by_xpath('//*[@id="select2-lookup-string-min-container"]/span').click()
    search = driver.find_element_by_xpath('/html/body/span/span/span[1]/input')

    # Sleep for 3 seconds to load whole page
    time.sleep(1)

    search.send_keys(company_to_search)
    #option = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[.='%s']" % company_to_search)))
    search.send_keys(Keys.ENTER)

    # Execute script to scroll down the page and make sure that we are loading the full page
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
    # Sleep for 3 seconds to load whole page
    time.sleep(3)

    "//*[@id="main-spaceholder"]/section[5]/div/div[1]/div[3]/div[1]/div/div[2]/span/span
    ## ENERGY AND CLIMATE RATING
    energy_class = driver.find_element_by_xpath('//*[@id="main-spaceholder"]/section[5]/div/div[1]/div[3]/div[1]/div/div[2]/span/span')
    energy = energy_class.text


    ## ENVIRONMENT POLICY AND REPORTING
    environment_class = driver.find_element_by_xpath('//*[@id="main-spaceholder"]/section[5]/div/div[1]/div[3]/div[2]/div/div[2]/span/span')
    environment = environment_class.text


    ## RESOURCE MANAGEMENT
    resource_class = driver.find_element_by_xpath('//*[@id="main-spaceholder"]/section[5]/div/div[1]/div[3]/div[3]/div/div[2]/span/span')
    resource = resource_class.text


    company_data = {'company': company_to_search,'energy_rating': energy,'environment_rating': energy,'resource_rating': resource}


    ESG_writer.writerow(company_data)
    drive.close()



#user_file.close()
post_file.close()



company_data
