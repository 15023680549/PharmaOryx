import requests
from bs4 import BeautifulSoup
import csv

body_url=[]
urlList=[['CHEMICAL THREATS','https://cbrnecentral.com/category/biological/outbreak-news'],
         ['RADIOLOGICAL-NUCLEAR','https://cbrnecentral.com/category/radiological-nuclear'],
         ['FORENSICS','https://cbrnecentral.com/category/forensics'],
         ['EXPLOSIVES','https://cbrnecentral.com/category/explosives'],
         ['TECH + EQUIPMENT','https://cbrnecentral.com/category/technology-equipment'],
         ['UNMANNED SYSTEMS','https://cbrnecentral.com/category/technology-equipment']]

def getBodyUrl():
    for url in urlList:
        topics = url[0]
        url = url[1]
        pageNo = 1
        while True:
            response = requests.get(url+'/page/'+str(pageNo)+'/');
            print(pageNo)
            if response.status_code==200:
                #取每页文章标题和链接
                soup = BeautifulSoup(response.text, 'html.parser')
                entry_body = soup.find_all('div',class_='entry-body')
                for div in entry_body:
                    title = div.a.string
                    url = div.a.attrs['href']
                    body_url.append([topics,title,url,url+'page/'+str(pageNo)+'/'])
                    # dl = ''
                    # xl = ''
                    # if i != 1:
                    #     dl = div.h2.a.string  # 大类
                    #     if div.dt:
                    #         xl = div.dt.string  # 小类
                    #     # print(div.prettify())
                    #     for em in div.findAll('em'):
                    #         urls.append([dl, xl, em.a.string, 'https://www.chemicalbook.com' + em.a.attrs['href'], lx])
                    # i += 1
                if pageNo==1:
                    break
            else:
                break
            pageNo+=1

bodys = []

def getBody(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    body = soup.find('div',class_='entry-inner')
    #作者
    author = body.header.find('span',class_='entry-author').a.text
    #时间
    time = body.header.find('time',class_='entry-date').text
    #内容
    content = body.div.text
    return [author,time,content]

#存储数据之csv
def tocsv(fileNmae,rows):
    with open('E:\\work\\djrm\\ykb\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

bodys = []
if __name__ == '__main__':
    getBodyUrl()
    for url in body_url:
        body = getBody(url[2])
        print(url)
        print(body)
        tocsv('cbrne.csv', [[url[0],url[1],url[2],url[3],body[0],body[1],body[2]]])