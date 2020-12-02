from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('C:/Program Files/chromedriver.exe')
wait = WebDriverWait(driver, 10)

## list of companies for future
companies = ['TESLA, INC.']
for company in companies:


company_to_search = 'TESLA, INC.'
url = 'https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/issuer/verizon-communications-inc/IID000000002188695'


driver.get(url)
search = wait.until(EC.visibility_of_element_located((By.ID, "_esgratingsprofile_keywords")))
search.send_keys(company_to_search)
option = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[.='%s']" % company_to_search)))
option.click()



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


company_data
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

## company name
company_name_element = driver.find_element_by_class_name('header-company-title')
company_name = company_name_element.text

## rating score
rating_class = driver.find_element_by_class_name('ratingdata-company-rating')
rating_class_elements = rating_class.get_attribute('class').split()
rating_class_elements.remove('ratingdata-company-rating')
esg_rating = rating_class_elements[0].split('-')[-1]

## number of companies in industry
descriptive_class = driver.find_element_by_class_name('esg-rating-paragraph')
descriptive_class_elements = descriptive_class.get_attribute('class').split()



company_data = {
    'name': company_name,
    'esg': esg_rating
}
