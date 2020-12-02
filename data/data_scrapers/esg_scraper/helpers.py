import time
import requests
from bs4 import BeautifulSoup
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def search_company(keyword):
    search_url = 'https://www.msci.com/esg-ratings?p_p_id=esgratingsprofile&' \
        'p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchEsgRatingsProfiles&' \
        'p_p_cacheability=cacheLevelPage&_esgratingsprofile_keywords={}'.format(keyword)
    search_response = requests.get(search_url)
    search_json = search_response.json()
    # We get the first result, since it is the best match for the searched term
    result = search_json[0]
    print(result)
    company_meta = {
        'id': result['url'],
        'name': result['encodedTitle']
    }
    return company_meta

def get_rating(company_meta):
    company_url = 'https://www.msci.com/esg-ratings/issuer/{name}/{id}'.format(**company_data)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(company_url)
    # Execute script to scroll down the page and make sure that we are loading the full page
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
    # Sleep for 3 seconds to load whole page
    time.sleep(3)

    class_element = driver.find_element_by_class_name('ratingdata-company-rating')
    class_element_classses = class_element.get_attribute('class').split()
    class_element_classses.remove('ratingdata-company-rating')
    esg_class = class_element_classses[0].split('-')[-1]

    company_name_element = driver.find_element_by_class_name('header-company-title')
    company_name = company_name_element.text

    company_data = {
        'name': company_name,
        'esg': esg_class
    }
    return esg_class

# Given a keywoard, returns the ESG rating for the first result when searching using the MSCI company
# search. Given this, the user should try using the most accurate name possible.
def get_company_rating(keywoard):
    company_meta = search_company(keywoard)
    company_data = get_rating(company_meta)
    return company_data



company_url = 'https://www.msci.com/esg-ratings/issuer/{name}/{id}'.format(**company_data)
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(company_url)
# Execute script to scroll down the page and make sure that we are loading the full page
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;')
# Sleep for 3 seconds to load whole page
time.sleep(3)

class_element = driver.find_element_by_class_name('ratingdata-company-rating')
class_element_classses = class_element.get_attribute('class').split()
class_element_classses.remove('ratingdata-company-rating')
esg_class = class_element_classses[0].split('-')[-1]

company_name_element = driver.find_element_by_class_name('header-company-title')
company_name = company_name_element.text

company_data = {
    'name': company_name,
    'esg': esg_class
}
