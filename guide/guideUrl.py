#-*- coding : utf-8-*-
# coding:utf-8
import os
import json
import requests

dir=os.getcwd()


class GuideUrl:
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        self.rows=[]
        self.qx={500109:'bbq',500105:'jbq',500116:'jjq',500119:'ncq',500242:'yyxxx',500113:'bnq',500114:'qjq'}
        # self.proxies={'https':'https://115.223.11.212:50000',
        #               'http':'http:36.99.35.138:82',
        #               'http':'http://223.113.80.158:9091'}

    def get_html(self,url):
        res = requests.get(url, headers=self.headers)
        return res.json()

    #公共服务清单
    def ggfwUrl(self,orgCode):
        for num in range(1,1000):
            print(num)
            # url = 'https://cqykb.cq.gov.cn/pc/xindian/country/publicCatalog?useLevel=&taskName=&pageNum='+str(num)+'&pageSize=10&type=2&ouCode=&areaCode='+str(orgCode)+'&fwlb='
            url = 'https://cqykb.cq.gov.cn/pc/xindian/country/v2/publicCatalog?useLevel=&taskName=&pageNum='+str(num)+'&pageSize=10&type=2&ouCode=&areaCode='+str(orgCode)+'&fwlb='
            # res = requests.get(url,headers=self.headers,proxies=self.proxies)
            res = requests.get(url,headers=self.headers)
            data = res.json()['data']
            if(len(data['list'])==0):
                return self.rows
            list = data['list']
            for li in list:
                if(li['itemCount']==1):
                    for item in li['itemList']:
                        self.rows.append([item['taskName'],item['rowGuid'],'https://zwykb.cq.gov.cn/qxzz/'+self.qx[orgCode]+'/bszn/?rowGuid='+item['rowGuid']])
                else:
                    #在有下级的情况下
                    catalogId = li['catalogId']
                    url = 'https://cqykb.cq.gov.cn/pc/xindian/country/publicChildDetail?catalogId='+catalogId+'&useLevel=&taskName=&type=2&ouCode=&areaCode='+str(orgCode)+'&fwlb='
                    # res = requests.get(url,headers=self.headers,proxies=self.proxies)
                    res = requests.get(url,headers=self.headers)
                    print(res.text)
                    data = res.json()
                    list = data['data']
                    print(data)
                    for item in list:
                        # print(item['taskName'])
                        self.rows.append([item['taskName'],item['rowGuid'],'https://zwykb.cq.gov.cn/qxzz/'+self.qx[orgCode]+'/bszn/?rowGuid='+item['rowGuid']])

    def xzqlUrl(self,orgCode):
        for num in range(1,1000):
            print(num)
            url = 'https://cqykb.cq.gov.cn/pc/xindian/country/v2/powerCatalog?taskType=&useLevel=&taskName=&pageNum='+str(num)+'&pageSize=10&type=2&ouCode=&areaCode='+str(orgCode)
            #测试公安局地址
            # url = 'https://cqykb.cq.gov.cn/pc/xindian/country/v2/powerCatalog?taskType=01&useLevel=&taskName=&pageNum='+str(num)+'&pageSize=10&type=2&ouCode=5001091029&areaCode=500109'
            # res = requests.get(url,headers=self.headers,proxies=self.proxies)
            res = requests.get(url,headers=self.headers)
            data = res.json()['data']
            if(data==None):
                return self.rows;
            if(data['itemCount']==0 or len(data['list']) == 0):
                return self.rows
            list = data['list']
            # print(data['list'])
            for li in list:
                # print(li['taskName'])
                if(li['itemCount']==1):
                    for item in li['itemList']:
                        self.rows.append([item['taskName'],item['rowGuid'],'https://zwykb.cq.gov.cn/qxzz/'+self.qx[orgCode]+'/bszn/?rowGuid='+item['rowGuid']])
                else:
                    #在有下级的情况下
                    catalogId = li['catalogId']
                    url = 'https://cqykb.cq.gov.cn/pc/xindian/country/v2/powerChildDetail?catalogId='+catalogId+'&taskType=&useLevel=&taskName=&type=2&ouCode=&areaCode='+str(orgCode)
                    # url = 'https://cqykb.cq.gov.cn/pc/xindian/country/powerChildDetail?catalogId='+catalogId+'&taskType=&useLevel=&taskName=&type=2&ouCode=&areaCode='+str(orgCode)+'&fwlb='
                    # res = requests.get(url,headers=self.headers,proxies=self.proxies)
                    res = requests.get(url,headers=self.headers)
                    data = res.json()
                    li2 = data['data']
                    if(data==None or data['code'] !=200):
                        continue;
                    if(li2['list']!=None):
                        for li22 in li2['list']:
                            for li222 in li22['itemList']:
                                # print('三级:' + li222)
                                self.rows.append([li222['taskName'], li222['rowGuid'],
                                                  'https://zwykb.cq.gov.cn/qxzz/' + self.qx[orgCode] + '/bszn/?rowGuid=' +
                                                  li222['rowGuid']])
                    for item in li2['itemList']:
                        # print('二级:'+item)
                        self.rows.append([item['taskName'], item['rowGuid'],
                                          'https://zwykb.cq.gov.cn/qxzz/' + self.qx[orgCode] + '/bszn/?rowGuid=' +
                                          item['rowGuid']])

                    # for item in list:
                        # print(item['taskName'])
                        # self.rows.append([item['taskName'],item['rowGuid'],'https://zwykb.cq.gov.cn/qxzz/'+self.qx[orgCode]+'/bszn/?rowGuid='+item['rowGuid']])

if __name__ == '__main__':
    url='https://cqykb.cq.gov.cn/pc/xindian/country/publicCatalog?useLevel=&taskName=&pageNum=27&pageSize=10&type=2&ouCode=&areaCode=500105&fwlb='
    # get_html('https://cqykb.cq.gov.cn/pc/xindian/country/publicCatalog?useLevel=&taskName=&pageNum=27&pageSize=10&type=2&ouCode=&areaCode=500105&fwlb=')
    # GuideUrl.forUrl(self,'500105')
    # GuideUrl().forUrl(500105)