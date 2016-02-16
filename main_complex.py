# -*- coding: utf-8 -*-

import requests
import bs4
import time
import codecs
import xlwt

'''
<dt>总建面</dt><dd>220000平方米（大型小区）</dd>  0
<dt>总户数</dt><dd>1717户</dd>                  1
<dt>建造年代</dt><dd>2010-12</dd>               2
<dt>容积率</dt><dd>2.15</dd>                    3
<dt>出租率</dt><dd id="rate">暂无数据</dd>       4
<dt>停车位</dt><dd>1600</dd>                    5
<dt>绿化率</dt><dd>20%（绿化率适中）</dd>         6

'''

class Tool:

	def __init__(self,cityName):
		self.rootUrl = 'http://www.anjuke.com/'
		self.baseUrl = self.rootUrl + cityName + '/cm/'
		self.checkHref = self.rootUrl + cityName + '/'
		self.blUrlModle = 'http://'+cityName+'.anjuke.com/community/view/'
		self.cityName = cityName
		self.cityNameCh = u'杭州市'
		self.ak = '7dXXzhBmlscv2gowbj3I3ouX'
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

	def getuidFromBaiduApi(self,location):
		try:
        	
			baiduGeoUrl = 'http://api.map.baidu.com/geocoder/v2/?ak=' + self.ak + '&location=' + location + '&output=json&pois=1'
			uidStr = 'uid'
			response = requests.get(baiduGeoUrl)
			result = response.text
			json_str = result
			uidIndex = json_str.index(uidStr) + len(uidStr) + 3  #":"35a08504cb51b1138733049d"
			potIndex = json_str.find(',',uidIndex) - 1 #35a08504cb51b1138733049d"
			uidValue = json_str[uidIndex:potIndex]
		except:
			uidValue = 'none'
		return uidValue




	def getOnePageEstates(self,pageUrl,areaName):
		soup = self.sendRequest(pageUrl)
		f = codecs.open(areaName+'_e.txt','a','utf-8')
		districts = soup.select('ul.P3 a')
		if(len(districts)):
			for district in districts:
				href = district.get("href")
				if(self.checkHref in href):
					cmCode = self.getcrmCodeFromHref(href)
					if(cmCode.isdigit()):
						
						blValue = self.getEstatesBL(cmCode,2)
						location = self.getEstatesBL(cmCode,0)
						uid = self.getuidFromBaiduApi(location)
						areaNameCh = areaName + u'区'
						resultStr = "%s %s %s %s %s" % (self.cityNameCh,areaNameCh,district.string,blValue,uid)
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
	

	#addressUrl href="http://hangzhou.anjuke.com/map/sale/?#l1=30.3421789&l2=120.083714&l3=18&commid=193851&commname=金地自在城"
	def getEstatesBL(self,code,kind):
		#request  http://hangzhou.anjuke.com/community/view/160845
		blUrl = self.blUrlModle + code
		time.sleep(0.5)  # sleep
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
			if(kind > 1):
				otherInfo = self.getOtherInfoOfEstate(soup)
				blValue = otherInfo + ' ' + l1Value + ' ' + l2Value
			else:
				blValue = l1Value + ',' + l2Value
			return blValue


	def getOtherInfoOfEstate(self,soup):
		rightTags = soup.find_all(class_='comm-r-detail float-r')
		priceTags = soup.select('.comm-avg-price')
		if(len(priceTags)):
			price = priceTags[0].string
		else:
			price = none
		result = price + u'元/平方 '
		for rightTag in rightTags:
			ddTags = rightTag.select('dd')
			
			row = 0
			for ddTag in ddTags:
				if(row == 1 or row == 2):
					ddTagValue = ddTag.string
					result = result + ddTagValue + ' '
				row += 1
		return result

        
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
spider.oneStart('binjiang')


	
		
    	

