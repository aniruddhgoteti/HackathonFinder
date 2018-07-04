from time import sleep
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

Client= MongoClient('localhost', 27017)
db= Client["hackathons"]

hack= db.hack_finder


driver = webdriver.Chrome()
driver.get("https://www.postscapes.com/")

search_query= driver.find_element_by_name('s')
search_query.send_keys('hackathon')
search_query.send_keys(Keys.RETURN)
sleep(3)

title = driver.find_elements_by_xpath('//a[@rel="bookmark"]')[0].text

sel= Selector(text= driver.page_source)
url = sel.xpath('//h2[@class="entry-title"]//a/@href').extract_first()

hack_data = {
'Image':"N/A",
'Title of event': title,
'Date': "N/A",
'Time': "N/A",
'Location': "Online",
'GPS': "N/A",
'Event Description': "N/A",
'Prizes': "N/A",
'Schedule': "N/A",
'Sponsor': "N/A",
'Event URL': url,
}

result= hack.insert_one(hack_data)
print(format(result.inserted_id))

driver.quit()


