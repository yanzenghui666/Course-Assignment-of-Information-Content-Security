#coding=utf-8
import requests                     # 获取页面信息
from bs4 import BeautifulSoup       # 解析页面信息

url='https://tianchi.aliyun.com/competition/gameList/activeList'
r = requests.get(url)            # 获取页面HTML
content = r.text
soup = BeautifulSoup(content,'html.parser')         # 创建soup对象
titleArr = []                   # 保存标题
contentArr = []                 # 保存内容
list = soup.find(id='forSEO')
for item1 in list.find_all('a'):
    titleArr.append(item1.text)
for item2 in list.find_all('p'):
    contentArr.append(item2.text)
fp = open('test.txt','w')
for i in range(len(titleArr)):
    fp.write(titleArr[i-1] + "\n")
    fp.write(contentArr[i-1] + "\n\n")
fp.close()