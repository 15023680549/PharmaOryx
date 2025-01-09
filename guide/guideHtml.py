# -*- coding : utf-8-*-
# coding:utf-8
from multiprocessing import Pool, Manager
import aiohttp
import asyncio
import time

#多线程，解析html结果
def main_parse_html():
    p = Pool(2)
    i = 0
    for html in htmls:
        i += 1
        p.apply_async(multi_parse_html, args=(html, i))
    p.close()
    p.join()

    # with Pool(2) as p:
    #     for i, html in enumerate(self.htmls):
    #         print(i)
    #         p.apply_async(self.multi_parse_html, args=(html, i + 1, rows))
    #     p.close()
    #     p.join()

# def __init__(self, urls):
#     self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
#     self.htmls = []
#     self.sem = asyncio.Semaphore(10)  # 信号量，控制协程数量，防止爬的过快
#     self.urls = urls

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
htmls=[]
rows=[]
urls=[]
sem = asyncio.Semaphore(10)  # 信号量，控制协程数量，防止爬的过快

#获取请求json
async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(headers=headers) as session:  # 获取session
            async with session.get('https://cqykb.cq.gov.cn/pc/xindian/item_guid/guid_detail?rowGuid='+url[1]) as resp:  # 提出请求
                html = await resp.json()  # 直接获取到bytes
                htmls.append([html['data'], url[2]])
                print(f'异步获取 {url[0]}, {url[2]}')

#协程，批量请求链接
def main_get_html():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html, cnt):
    print(f'第 {cnt} 个 html ----------- date: {time.time()}')
    try:
        parsed_list = util_parse_html(html)  # 假设util_parse_html是一个返回解析后的数据的函数
        rows.append(parsed_list)
    except Exception as e:
        error_info = f'Error in parsing HTML {cnt}: {str(e)}'
        print(error_info)
    # rows.append(parsed_list)

def util_parse_html(html):
    url = html[1]
    guidDetail = html[0]['guidDetail']
    print(guidDetail)
    taskName = guidDetail['taskName']
    # 这里是解析 HTML 的逻辑，返回解析后的数据
    # 这个函数需要你自己实现
    return [taskName]  # 返回一个列表

# 示例使用
if __name__ == "__main__":
    urls = [['受理关于供水水质的投诉','349c4706-dec1-4282-a6c4-e2f23be01506','https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?rowGuid=349c4706-dec1-4282-a6c4-e2f23be01506'],['公共文化场馆展览展示及讲座培训','400a279d-fb6b-4236-9aee-130f8d99529a','https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?rowGuid=400a279d-fb6b-4236-9aee-130f8d99529a']]
    # tool = MyGetHtmlTool(urls)

    # 使用 Manager 来管理进程间共享的列表
    with Manager() as manager:
        rows = manager.list()
        # htmls = manager.list()  # 创建一个共享的错误信息列表
        main_get_html()  # 获取 HTML
        main_parse_html()  # 解析 HTML

        # 输出结果
        for row in rows:
            print(row)
# -*- coding : utf-8-*-
# coding:utf-8
from multiprocessing import Pool, Manager
import aiohttp
import asyncio
import time

#多线程，解析html结果
def main_parse_html():
    p = Pool(2)
    i = 0
    for html in htmls:
        i += 1
        p.apply_async(multi_parse_html, args=(html, i))
    p.close()
    p.join()

    # with Pool(2) as p:
    #     for i, html in enumerate(self.htmls):
    #         print(i)
    #         p.apply_async(self.multi_parse_html, args=(html, i + 1, rows))
    #     p.close()
    #     p.join()

# def __init__(self, urls):
#     self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
#     self.htmls = []
#     self.sem = asyncio.Semaphore(10)  # 信号量，控制协程数量，防止爬的过快
#     self.urls = urls

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
htmls=[]
rows=[]
urls=[]
sem = asyncio.Semaphore(10)  # 信号量，控制协程数量，防止爬的过快

#获取请求json
async def get_html(url):
    async with sem:
        async with aiohttp.ClientSession(headers=headers) as session:  # 获取session
            async with session.get('https://cqykb.cq.gov.cn/pc/xindian/item_guid/guid_detail?rowGuid='+url[1]) as resp:  # 提出请求
                html = await resp.json()  # 直接获取到bytes
                htmls.append([html['data'], url[2]])
                print(f'异步获取 {url[0]}, {url[2]}')

#协程，批量请求链接
def main_get_html():
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

def multi_parse_html(html, cnt):
    print(f'第 {cnt} 个 html ----------- date: {time.time()}')
    try:
        parsed_list = util_parse_html(html)  # 假设util_parse_html是一个返回解析后的数据的函数
        rows.append(parsed_list)
    except Exception as e:
        error_info = f'Error in parsing HTML {cnt}: {str(e)}'
        print(error_info)
    # rows.append(parsed_list)

def util_parse_html(html):
    url = html[1]
    guidDetail = html[0]['guidDetail']
    print(guidDetail)
    taskName = guidDetail['taskName']
    # 这里是解析 HTML 的逻辑，返回解析后的数据
    # 这个函数需要你自己实现
    return [taskName]  # 返回一个列表

# 示例使用
if __name__ == "__main__":
    urls = [['受理关于供水水质的投诉','349c4706-dec1-4282-a6c4-e2f23be01506','https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?rowGuid=349c4706-dec1-4282-a6c4-e2f23be01506'],['公共文化场馆展览展示及讲座培训','400a279d-fb6b-4236-9aee-130f8d99529a','https://zwykb.cq.gov.cn/qxzz/jbq/bszn/?rowGuid=400a279d-fb6b-4236-9aee-130f8d99529a']]
    # tool = MyGetHtmlTool(urls)

    # 使用 Manager 来管理进程间共享的列表
    with Manager() as manager:
        rows = manager.list()
        # htmls = manager.list()  # 创建一个共享的错误信息列表
        main_get_html()  # 获取 HTML
        main_parse_html()  # 解析 HTML

        # 输出结果
        for row in rows:
            print(row)
