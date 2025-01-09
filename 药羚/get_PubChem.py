#-*- coding : utf-8-*-
# coding:utf-8

import time
from lxml import etree
from multiprocessing import Pool
import requests
import aiohttp
import asyncio
import pymysql
import re
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET


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



#获取url中CID
def get_CID(url):
    return re.findall("\d+",url)[0]

#保存html内容到文件
def save_xml(html,CID):
    # 保存json文件
    file_name = 'compound_CID_' + str(CID) + '.xml'
    f = open('C:\\Users\\yong.jiang3\\Desktop\\pubchem_data\\' + file_name, 'w', encoding='utf-8_sig')
    f.write(html)
    f.close()

async def get_html(url):
    #with(await sem):
    async with sem: #
        #async with是异步上下文管理器
        async with aiohttp.ClientSession(trust_env = True) as session:  #获取session
            #async with session.request('GET',url.format(10)) as resp:  #提出请求
            async with session.request('GET', url) as resp:  # 提出请求
                html=await resp.text() #直接获取到bytes
                htmls.append(html)
                save_xml(html,get_CID(url)) #保存xml
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
    #print(html)

#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()

#顺序获取
def get_html2(CID):
    resp=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(CID) + "/XML")
    html=resp.text
    save_xml(html, get_CID(url))  # 保存xml

if __name__ == '__main__':
    # 测试
    # CID=0
    htmls=['sfd','sdf','sdf','sd','sdf','sdf','sdf','sdf']
    main_parse_html()
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