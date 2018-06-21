from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import ssl


my_url="https://hackevents.co/hackathons"
req= Request(my_url,headers={'User-Agent': 'Mozilla/5.0'})
uclient=urlopen(req).read()

page_soup=soup(uclient, "html.parser" )
containers=page_soup.findAll("div",{"class":"hackathon"})

for container in containers:

	month= container.div.div.text.strip()

	day= container.div.findAll("div",{"class":"date-day-number"})[0].text.strip()

	