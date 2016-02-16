# -*- coding: utf-8 -*-

import requests
import bs4
import time
import codecs

class Tool:

	def __init__(self,cityName):
		self.rootUrl = 'http://www.anjuke.com/'
		self.baseUrl = self.rootUrl + cityName + '/cm/'
		self.checkHref = self.rootUrl + cityName + '/'
		self.blUrlModle = 'http://'+cityName+'.anjuke.com/community/view/'
		self.cityName = cityName
		self.ak = 'E4805d16520de693a3fe707cdc962045'
		self.l1 = 'l1='
		self.l2 = 'l2='
		self.l3 = 'l3='
		

	def sendRequest(self,url):
		response = requests.get(url)
		soup = bs4.BeautifulSoup(response.text)
		return soup

	def getAreasHref(self):
		response = requests.get(self.baseUrl)
		soup = bs4.BeautifulSoup(response.text)
		areas = soup.select('.P2a')
		herfList = []
		for area in areas:
			
			href = area.get('href')
			herfList.append(href)
		return herfList


	def getcrmCodeFromHref(self,href):
		str1= href
		str2= self.checkHref + 'cm'
		str2Len = len(str2)
		endIndex = len(str1) - 1
		code = str1[str2Len:endIndex]
		return code





	def getOnePageEstates(self,pageUrl,areaName):
		soup = self.sendRequest(pageUrl)
		f = codecs.open(areaName+'.txt','a','utf-8')
		districts = soup.select('ul.P3 a')
		for district in districts:
			href = district.get("href")
			if(self.checkHref in href):
				cmCode = self.getcrmCodeFromHref(href)
				if(cmCode.isdigit()):
					
					blValue = self.getEstatesBL(cmCode)
					resultStr = "('%s','%s','%s')" % (self.cityName,areaName,district.string)
					f.write(resultStr + '\n')
		f.close()
	
								


	def getOneAreaEstates(self,areaUrl,areaName):
		count = 0
		while count < 2:
			count += 1;
			str_count = str(count)
			pageUrl = areaUrl + 'p'+str_count + '/'
			response = requests.get(pageUrl)
			soup = bs4.BeautifulSoup(response.text)
			nextPageTag = soup.find_all(class_='nolink nextpage')
			if len(nextPageTag):
				break
			self.getOnePageEstates(pageUrl,areaName)
	

#href="http://hangzhou.anjuke.com/map/sale/?#l1=30.3421789&l2=120.083714&l3=18&commid=193851&commname=金地自在城"
	def getEstatesBL(self,code):
		blUrl = self.blUrlModle + code
		
		soup = self.sendRequest(blUrl)
		tag = soup.select('div.border-info a[class="comm-icon"]')

		if(len(tag)):
			blHref = tag[0].get("href")
			l1IndexBegin = blHref.index(self.l1) + len(self.l1)
			l2Index = blHref.index(self.l2)
			l1End = l2Index - 1
			l2IndexBegin = l2Index + len(self.l2)
			l3Index = blHref.index(self.l3)
			l2End = l3Index - 1
			l1Value = blHref[l1IndexBegin:l1End]
			l2Value = blHref[l2IndexBegin:l2End]
			blValue = "'%s','%s'" % (l1Value,l2Value)
			return blValue

        
	def oneStart(self,areaName):
		url = self.baseUrl + areaName + '/'
		self.getOneAreaEstates(url,areaName)
    	
    	


	def start(self):
		soup = self.sendRequest(self.baseUrl)
		areas = soup.select('.P2a')
		herfList = []
		for area in areas:
			href = area.get('href')
			areaName = area.string
			self.getOneAreaEstates(href,areaName)

    


spider = Tool('hangzhou')
spider.oneStart('xiaoshan')


	
		
    	

