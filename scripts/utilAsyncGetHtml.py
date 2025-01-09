#-*- coding : utf-8-*-
# coding:utf-8

import aiohttp
import asyncio

import json

sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

async def get_html(url):
    async with sem: #
        async with aiohttp.ClientSession(headers=headers) as session:  #获取session
            data = {"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"id":url[1],"basicCode":"","orgCode":"","isQueryCons":1,"matterId":""}}
            data = json.dumps(data)
            async with session.post('https://ykbapp.cq.gov.cn:8082/gml/web10002',data=data) as resp:  # 提出请求
                html=await resp.json() #直接获取到bytes
                # htmls.append([html['C-Response-Body'],url[2]])
                name=json.loads(html['C-Response-Body'])
                print('异步获取%s.'% name['name'],url[2])
                return [html['C-Response-Body'],url[2]]