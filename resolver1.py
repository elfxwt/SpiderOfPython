import requests
import bs4


try:
	response = requests.get('http://www.anjuke.com/杭州/cm/gongshu/p4/')
	soup = bs4.BeautifulSoup(response.text)
	nextPageTag = soup.find_all(class_='nolink nextpage')
	while 1> 0:
		print "12"
		if len(nextPageTag):
			print "34"
			break
   
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason