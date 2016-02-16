# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup

try:
    soup = BeautifulSoup(open('index.html'))
    districts = soup.select('.P2a')
    for district in districts:
    	disName = district.string
    	disString = unicode(disName, 'utf-8')
    	exceptStr = u"大全"
    	if disString.find(exceptStr) != -1:
    	    print disString.string

   
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason






        
page = "p1"
cityName = "杭州"
baseUrl = "http://www.anjuke.com/"
url = baseUrl+"杭州/cm/gongshu/" + str(page)
checkHref = baseUrl + cityName
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text)
districts = soup.select('.P3 a')
for district in districts:
	href = district.get("href")
	if(checkHref in href):
		print district.string