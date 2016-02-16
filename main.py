# -*- coding: utf-8 -*-
import xlwt
import requests
import bs4





url = 'http://hangzhou.anjuke.com/community/view/504500'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text)
priceTags = soup.select('.comm-avg-price')
if(len(priceTags)):
	price = priceTags[0].string
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
				result = result + emTags[0].string + ' '
			else:
				result = result + u'暂无数据' + ' '
		else:
			result = result + lddTag.string + ' '
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
		rddTagValue = rddTag.string
		result = result + rddTagValue + ' '
resultList = result.split(' ')	
for value in resultList:
	print value

		





	



