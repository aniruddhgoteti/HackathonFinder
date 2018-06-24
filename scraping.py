from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import ssl
from geopy import Nominatim
from tabulate import tabulate


geolocator = Nominatim()
my_url="https://hackevents.co/hackathons"

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(my_url)

#filename= "hack.csv"
#f= open(filename, "wb")

#headers= "date, title, location, address"

#f.write(headers).encode()

#To Scrape
"""Image or Logo for the event
Name/Title of event
Date (DD/MM/YYYY)
Time: 
Location: Address/location 
GPS Coordinates Preferred 
Event Description
Prizes (if applicable)
Schedule (if applicable)
Created by/Sponsor
Event URL """ 


page_soup=soup(driver.page_source, 'html.parser')

#total_page=soup.findAll("div",{"class":"hackathons"})

containers=page_soup.findAll("div",{"class":"hackathon"})


datalist = [] #empty list
 

for container in containers:

	date= container.findAll("span", {"class":"info-date"})[0].text.strip()

	title= container.findAll("a",{"class":"title"})[0].text.strip()

	city= container.findAll("span", {"class":"city"})[0].text.strip()

	country= container.findAll("span", {"class":"country"})[0].text.strip()
    
    


	links =[] 
	for link in container.findAll('a'):
		links.append(link.get('href'))


	#driver.get("https://hackevents.co"+links[1])

	#page_soup_1= soup(driver.page_source, 'lxml')

	#box= page_soup_1.findAll("div", {"id":"map"})

	#address= page_soup_1.findAll("div", {"id":"over_map"})[0].text.strip().encode("utf-8")
	#address_geo= print(address.latitude,address.longitude)

	#driver.execute_script("window.history.go(-1)") 

	print("date" + date)
	print("title"+ title)
	print("city"+ city)


	#f.write(date + "," + title + "," + city + "," + b'\n')


#f.close()










