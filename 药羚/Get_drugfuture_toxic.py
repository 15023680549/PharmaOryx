import aiohttp
import asyncio
import urllib.request
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
import re
import os

htmls=[]
urls=[
    #'https://www.drugfuture.com/toxic/q1-q1.html',
      'https://www.drugfuture.com/toxic/q77-q568.html'
]

sem=asyncio.Semaphore(10)
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/102.0.5005.63 Safari/537.36'
}

dir=os.getcwd()

#保存文件
def sav_txt(html,filename):
    soup = BeautifulSoup(html, 'lxml')
    pre = soup.pre.string
    with open(dir + '\\toxic\\' + filename, 'w', encoding='utf-8_sig') as f:
        f.write(pre)

#处理pre标签中纯文本数据
def par_txt(pre):
    #切分文本每个模块
    print (pre.replace(' ','').splitlines())

async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(trust_env = True,headers=headers) as session:  #获取session
            async with session.request('GET', url,) as resp:  # 提出请求
                if resp.status==200 and resp.content_length>649:
                    html=await resp.text()
                    filename = url.split('/')[-1].replace('html', 'txt')
                    # 保存到文本
                    sav_txt(html, filename)


def main_get_htm():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html,cnt):
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify())  #格式化输出
    #tables = soup.findAll('table')


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
    for i in range(1,142):
        urls=[]
        htmls=[]
        for j in range(1,1000):
            urls.append('https://www.drugfuture.com/toxic/q'+str(i)+'-q'+str(j)+'.html')
        main_get_htm()
        #main_parse_html()  q142-q996.html