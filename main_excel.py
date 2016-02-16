# -*- coding: utf-8 -*-

import requests
import bs4
import time
import codecs
import xlwt

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
		self.cellNum = 21
		

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




	def getOnePageEstates(self,pageUrl,areaName,wb,sheet):
		soup = self.sendRequest(pageUrl)
		
		districts = soup.select('ul.P3 a')
		if(len(districts)):
			print len(districts)
			for district in districts:
				href = district.get("href")
				if(self.checkHref in href):
					cmCode = self.getcrmCodeFromHref(href)
					if(cmCode.isdigit()):
						blValue = self.getEstatesBL(cmCode,2)
						location = self.getEstatesBL(cmCode,0)
						uid = self.getuidFromBaiduApi(location)
						areaNameCh = areaName + u'区'
						resultStr = "%s %s %s %s %s" % (self.cityNameCh,areaNameCh,district.string,uid,blValue)
						resultList = resultStr.split(' ')
						cell = 0
						for result in resultList:
							if(result.isspace()):
								continue
							result = result.replace(' ','')
							sheet.write(row,cell,result)
							cell += 1
						row += 1
		
	
								




	def getOneAreaEstates(self,areaUrl,areaName):
		count = 0
		wb = xlwt.Workbook()
		sheet = wb.add_sheet('sheet1')
		row = 1
		cell = 0 
		row1 = sheet.row(0)
		row1.write(0,u'城市')
		row1.write(1,u'行政区')
		row1.write(2,u'小区名')
		row1.write(3,'bd_uid')
		row1.write(4,u'纬度')
		row1.write(5,u'经度')
		row1.write(6,u'房价(元／平方)')
		row1.write(7,u'小区名')
		row1.write(8,u'板块名')
		row1.write(9,u'地址')
		row1.write(10,u'开发商')
		row1.write(11,u'物业公司')
		row1.write(12,u'物业类型')
		row1.write(13,u'物业费用')
		row1.write(14,u'总建筑面积')
		row1.write(15,u'总户数')
		row1.write(16,u'建造年代')
		row1.write(17,u'容积率')
		row1.write(18,u'出租率')
		row1.write(19,u'停车位')
		row1.write(20,u'绿化率')
		while count > -1:
			count += 1;
			str_count = str(count)
			pageUrl = areaUrl + 'p'+str_count + '/'
			print pageUrl
			response = requests.get(pageUrl)
			soup = bs4.BeautifulSoup(response.text)
			nextPageTag = soup.find_all(class_='nolink nextpage')
			if len(nextPageTag):
				break
			self.getOnePageEstates(pageUrl,areaName,wb,sheet)
		wb.save(self.cityNameCh + '.xls')
	

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
				blValue = l1Value + ' ' + l2Value + ' ' +otherInfo 
 
			else:
				blValue = l1Value + ',' + l2Value
			return blValue


	#24626 嘉绿西苑 西湖文二西路 文二西路益乐路口 政府机构 嘉绿苑 普通住宅 0.4元 20000平方米（中型小区） 1000户 2000-01 90% 暂无数据 500 30%（绿化率高)  --15个
	def getOtherInfoOfEstate(self,soup):
		rightTags = soup.find_all(class_='comm-r-detail float-r')
		priceTags = soup.select('.comm-avg-price')
		if(len(priceTags)):
			price = priceTags[0].string.strip()
		else:
			price = none
		result = price + ' '

		'''
		<dd>嘉绿西苑</dd>
		<dd><a _soj="commaddrQ" alt="西湖" href="http://hangzhou.anjuke.com/sale/xihu/" target="_blank" title="西湖">
		                        西湖</a>
		<a _soj="commaddrB" alt="文二西路" href="http://hangzhou.anjuke.com/sale/wenerxilu/" target="_blank" title="文二西路">
		                        文二西路</a>
		</dd>
		<dd><em>文二西路益乐路口</em>
		<a _soj="commaddr" class="comm-icon" href="http://hangzhou.anjuke.com/map/sale/?#l1=30.28486&amp;l2=120.118288&amp;l3=18&amp;commid=504500&amp;commname=嘉绿西苑" target="_blank"></a></dd>
		<dd>政府机构</dd>
		<dd>嘉绿苑</dd>

		'''
		leftTags = soup.find_all(class_='comm-l-detail float-l')
		row = 0
		for leftTag in leftTags:
			lddTags = leftTag.select('dd')
			for lddTag in lddTags:
				if(row == 1):
					aTags = lddTag.select('a')
					aTagValue = ''
					if(len(aTags)):
						for aTag in aTags:
							aTagValue += aTag.string.strip()
					else:
						aTagValue = u'暂无数据'
					result = result + aTagValue + ' '
				elif (row == 2):
					emTags = lddTag.select('em')
					if(len(emTags)):
						result = result + emTags[0].string.strip().replace(' ','') + ' '
					else:
						result = result + u'暂无数据' + ' '
				else:
					result = result + lddTag.string.strip().replace(' ','') + ' '
				row += 1

		'''
		<dt>总建面</dt><dd>220000平方米（大型小区）</dd>  0
		<dt>总户数</dt><dd>1717户</dd>                  1
		<dt>建造年代</dt><dd>2010-12</dd>               2
		<dt>容积率</dt><dd>2.15</dd>                    3
		<dt>出租率</dt><dd id="rate">暂无数据</dd>       4
		<dt>停车位</dt><dd>1600</dd>                    5
		<dt>绿化率</dt><dd>20%（绿化率适中）</dd>         6

		'''
		rightTags = soup.find_all(class_='comm-r-detail float-r')
		for rightTag in rightTags:
			rddTags = rightTag.select('dd')

			for rddTag in rddTags:
				rddTagValue = rddTag.string.strip().replace(' ','')
				result = result + rddTagValue + ' '
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
spider.oneStart('gongshu')


	
		
    	

