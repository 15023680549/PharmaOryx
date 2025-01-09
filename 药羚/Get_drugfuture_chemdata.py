import aiohttp
import asyncio
import urllib.request
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
import re
import os
import xlsxwriter as xw
import csv

htmls=[]

urls=[]
rows=[]

sem=asyncio.Semaphore(10)
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}

dir=os.getcwd()

def get_url():
    srcs=['https://www.drugfuture.com/chemdata-a.html','https://www.drugfuture.com/chemdata-b.html','https://www.drugfuture.com/chemdata-c.html','https://www.drugfuture.com/chemdata-d.html','https://www.drugfuture.com/chemdata-e.html','https://www.drugfuture.com/chemdata-f.html','https://www.drugfuture.com/chemdata-g.html','https://www.drugfuture.com/chemdata-h.html','https://www.drugfuture.com/chemdata-i.html','https://www.drugfuture.com/chemdata-j.html','https://www.drugfuture.com/chemdata-k.html','https://www.drugfuture.com/chemdata-l.html','https://www.drugfuture.com/chemdata-m.html','https://www.drugfuture.com/chemdata-n.html','https://www.drugfuture.com/chemdata-o.html','https://www.drugfuture.com/chemdata-p.html','https://www.drugfuture.com/chemdata-q.html','https://www.drugfuture.com/chemdata-r.html','https://www.drugfuture.com/chemdata-s.html','https://www.drugfuture.com/chemdata-t.html','https://www.drugfuture.com/chemdata-u.html','https://www.drugfuture.com/chemdata-v.html','https://www.drugfuture.com/chemdata-w.html','https://www.drugfuture.com/chemdata-x.html','https://www.drugfuture.com/chemdata-y.html','https://www.drugfuture.com/chemdata-z.html']
    for src in srcs:
        async def fetch():
            async with aiohttp.request('GET',src,headers=headers) as resp:
                if resp.status == 200:
                    html=await resp.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table')
                    trs = table.findAll('tr')[1].findAll('a')
                    for a in trs:
                        urls.append('https://www.drugfuture.com'+a['href'])
        # 将协程放入时间循环
        loop=asyncio.get_event_loop()
        loop.run_until_complete(fetch())
    main_get_htm()


def save_text(filename,txt):
    with open(filename,'w', newline='',encoding="utf-8") as f:
        f.write(txt)

async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers) as session:  #获取session
            async with session.request('GET', url,) as resp:  # 提出请求
                if resp.status==200:
                    print(url+'访问成功')
                    htmls.append(await resp.text())


def main_get_htm():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html,cnt):
    rows=[]
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table').find('table')
    td=table.findAll('td')
    imgsrc='https://www.drugfuture.com/chemdata/'+td[1].a['href']
    imgname=dir+'\\chemdata\\'+imgsrc.split('/')[-1]
    filename=dir+'\\chemdata\\'+imgsrc.split('/')[-1].replace('emf','txt')
    print(imgsrc)
    print(imgname)
    urllib.request.urlretrieve(imgsrc,imgname)
    imgsrc=imgsrc.replace('.emf', '.gif').replace('stremf','structure')
    imgname=imgname.replace('emf', 'gif')
    urllib.request.urlretrieve(imgsrc, imgname)
    save_text(filename,table.text)
    print('第%d个html-----------date:%s'% (cnt,time.time()))


#多进程调用总函数，解析html
def main_parse_html():
    p=Pool(8)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i))
    p.close()
    p.join()

if __name__ == '__main__':
    get_url()
    main_parse_html()
    #10727个页面
