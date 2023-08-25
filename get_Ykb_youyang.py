#-*- coding : utf-8-*-
# coding:utf-8

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
import time
from lxml import etree
from multiprocessing import Pool
import requests
import aiohttp
import asyncio
import re
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET
from selenium import webdriver
import pymysql
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

urls=[]
htmls=[]
sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快
#conn=pymysql.connect(host='',user='',password='',port='',db='',charset='')
config={
    'creator':pymysql,
    'host':"",
    'port':"3306",
    'user':"",
    'password':"",
    'db':"",
    'charset':"utf8",
    'maxconnections':70, #连接池最大连接数
    'cursorclass':pymysql.cursors.DictCursor
}
#pool=pymysql(**config)
#conn=pool.connection()
#cursor=conn.cursor()

#cursor.execute("SELECT VERSION()")

#cursor.close()
#conn.close()
#print('链接数据库成功!')
#cursor=conn.cursor()

#存储数据之csv
def tocsv(fileNmae,rows):
    with open('E:\\work\\djrm\\ykb\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

async def get_html(url):
    #with(await sem):
    async with sem: #
        #async with是异步上下文管理器
        async with aiohttp.ClientSession(trust_env = True) as session:  #获取session
            #async with session.request('GET',url.format(10)) as resp:  #提出请求
            async with session.request('GET', url) as resp:  # 提出请求
                html=await resp.text() #直接获取到bytes
                htmls.append(html)
                print('异步获取%s下的html.'% url)
    #await asyncio.sleep(1)

#协程调用，请求网页
def main_get_html():
    loop=asyncio.get_event_loop()   #获取事件循环
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析html
def multi_parse_html(html,cnt):
    print('第%d个html-----------date:%s'% (cnt,time.time()))

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()

def login():
    # 登录页面
    driver.find_element_by_xpath('/html/body/div[3]/div[1]/ul/li[4]/div/div[2]').click()
    time.sleep(1)
    # 点击关闭按钮
    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button')
    driver.find_element_by_id('username').send_keys('15023680549')
    driver.find_element_by_id('password').send_keys('19920211.jY')


if __name__ == '__main__':
    driver = webdriver.Chrome()
    # driver.get('https://zwykb.cq.gov.cn/qxzz/yyxxx/fwqd/xzqlqd/');#行政权力清单
    driver.get('https://zwykb.cq.gov.cn/qxzz/yyxxx/fwqd/ggfwqd/');#公共服务清单
    time.sleep(2)
    time.sleep(30)
    total = driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[6]/a[6]').text
    #滑动滑块
    # driver.find_element_by_class_name('slider')
    for j in range(1, int(total)):
        print(j)
        for i in range(1,11):
            time.sleep(0.2)
            xpath='/html/body/div[4]/div[5]/div[2]/div['+str(i)+']/div/div[1]'
            # driver.find_element_by_xpath(xpath).click()
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            webdriver.ActionChains(driver).move_to_element(element).click().perform()
            # webdriver.ActionChains(driver).click(xpath).perform()
        time.sleep(3)
        for link in driver.find_elements_by_class_name('sx-zn'):
            href = 'https://zwykb.cq.gov.cn/qxzz/yyxxx/'+link.get_attribute('_href').replace('../../','')
            businessid = link.get_attribute('businessid')
            content = link.get_attribute('keywords')
            row=[content,businessid,href]
            tocsv('酉阳url.csv',[row])
        driver.find_element_by_class_name('yj-pga8').click()
        time.sleep(3)

    # htmls=['sfd','sdf','sdf','sd','sdf','sdf','sdf','sdf']
    # main_parse_html()
    # i=1
    # for f in range(1,101):
    #     urls.clear()
    #
    #     for i in range(i,i+10):
    #         CID = i
    #         #url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(CID) + "/XML"
    #         #urls.append(url)
    #         #get_html2(i)
    #         print(i)
    #     start=time.time()
    #     #main_get_html()
    #     #main_parse_html()
    #     print('总耗时:%0.5f秒'% float(time.time()-start))
    #     i+=1