import time
import requests
from bs4 import BeautifulSoup
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib import request

## first with one website
url = 'https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/issuer/verizon-communications-inc/IID000000002188695'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(page)
site_json=json.loads(soup.text)

type(page)



json_data = json.loads(page.text)


######################
import json
import urllib.request

connection = urllib.request.urlopen(url)

js = connection.read()

print(js)

info = json.loads(js.decode("utf-8"))





html = request.urlopen(url).read()
soup = BeautifulSoup(html,'html.parser')
site_json=json.loads(soup.text)
#printing for entrezgene, do the same for name and symbol
print([d.get('entrezgene') for d in site_json['hits'] if d.get('entrezgene')])


# this is the https request for data in json format
response_json = requests.get(url)
response_json.status_code
# only proceed if I have a 200 response which is saved in status_code
if (response_json.status_code == 200):
     response = response_json.json() #converting from json to dictionary using json library


if status != 200:
    print("An error has occured. [Status code", status, "]")
else:
    data = response.json() #Only convert to Json when status is OK.
    if not data["elements"]:
        print("Empty JSON")
    else:
        "You can extract data here"









## look at it all
print(soup.prettify())

## locating rating
loc = "highcharts-vynwils-9 > svg > g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-color-0.highcharts-tracker.highcharts-series-hover > g:nth-child(4) > text > tspan"
#highcharts-vynwils-9 > svg > g.highcharts-data-labels.highcharts-series-0.highcharts-column-series.highcharts-color-0.highcharts-tracker.highcharts-series-hover > g:nth-child(4) > text > tspan
rating = soup.select(loc)
print(rating)


## headlings
story_headline = soup.find_all("h1")[0].get_text()
print(story_headline)


loc = " div.esg-ratings-profile-header-coredata > div.header-company-title"
rating = soup.select(loc)
rating

story_date = soup.select("div.mini-info-list-wrap > ul > li > div")[0].get_text()
