#-*- coding : utf-8-*-
# coding:utf-8

import time
from multiprocessing import Pool
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import urllib.request
import csv
from csv import reader

try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET


urls=[]
htmls=[]
sem=asyncio.Semaphore(5)
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}

def get_url():
    with open('orgsyn.csv', 'r', encoding='utf-8') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            if(len(list_of_rows[i][0])>1):
                urls.append(list_of_rows[i][0])

#保存html内容到文件
def save_xml(html,CID):
    # 保存json文件
    file_name = 'compound_CID_' + str(CID) + '.xml'
    f = open('C:\\Users\\yong.jiang3\\Desktop\\pubchem_data\\' + file_name, 'w', encoding='utf-8_sig')
    f.write(html)
    f.close()

async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers) as session:
            async with session.request('GET', url) as resp:
                try:
                    url.index('pdf')
                    filename = 'C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\OrgSyn\\pdfs\\' + url[url.rfind('/')+1:]
                    print(filename)
                    with open(filename, 'wb') as f:
                        async for chunk in resp.content.iter_chunked(1000):
                            f.write(chunk)
                except:
                    filename=url[url.rfind('=')+1:]
                    html=await resp.text()
                    htmls.append([html,filename])
                print('异步获取%s下的html.'% url)

#协程调用，请求网页
def main_get_html():
    loop=asyncio.new_event_loop()   #获取事件循环
    asyncio.set_event_loop(loop)
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

#使用多进程解析html
def multi_parse_html(html,cnt):
    soup = BeautifulSoup(html[0], 'lxml')
    soup.prettify()
    procebody=soup.find('div',id='ctl00_MainContent_procedureBody')
    filename=html[1]
    imgs=soup.find('div',id='ctl00_MainContent_procedureBody').findAll('img')
    for img in imgs:
        img_src='http://orgsyn.org'+img['src']
        img_dir='C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\OrgSyn\\images\\'+img['src'][img['src'].rfind('/')+1:]
        urllib.request.urlretrieve(img_src,img_dir)
    with open('C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\OrgSyn\\htmls\\'+filename+'.html','w',encoding='utf-8_sig') as f:
        f.write(str(procebody.prettify()))
    with open('C:\\Users\\PharmaOryx-YJ\\Desktop\\data\\OrgSyn\\txt\\'+filename+'.txt','w',encoding='utf-8_sig') as f:
        f.write(procebody.text)
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

if __name__ == '__main__':
    start=time.time()
    get_url()
    # main_get_html()
    # main_parse_html()

    print('总耗时:%0.5f秒'% float(time.time()-start))
