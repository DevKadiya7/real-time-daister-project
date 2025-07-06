import requests
from bs4 import BeautifulSoup
url = "https://codewithharry.com" 


r = requests.get(url)
htmlcontent = r.content
# print(htmlcontent)

soup = BeautifulSoup(htmlcontent,"html.parser")
# print(soup.prettify())  # optional for formatting

# get the title from the html page
title =  soup.title

# print(title)
# print(soup)
# print(type(title))
# print(type(title.string))

# get all the paragraph from tha page
paras = soup.find_all('p')
# print(paras)

# get all the anchors tag from tha page
anchors= soup.find_all('a')
# print(anchors)

# print(soup.find('p'))

print(soup.find('p')['class']) #get class
print(soup.find('p'))    #get first elemnt of html page

# find all the elment of class lead

print(soup.find_all('p',class_="lead"))

# get the text from elments
print(soup.find('p').get_text)

# get alll the link from the pages
for link in anchors:
    print(link.get('href'))

