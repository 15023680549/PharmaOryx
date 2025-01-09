#-*- coding : utf-8-*-
# coding:utf-8
from scripts.utilMysql import MysqlTool
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

class GetGuide:
    def __init__(self,orgcode):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        self.url = 'https://cqykb.cq.gov.cn/pc/xindian/handle/getCategory?areaCode='+str(orgcode)+'&serviceObject='
        self.business = []
        self.orgList = []

    def Guide(self,object):
        if object=='gr':
            url = self.url+'1'
        elif object == 'fr':
            url = self.url+'2'
        res = requests.get(url,headers=self.headers)
        data = res.json()['data']
        for cate in data:
            #主题
            if cate['categoryId'] == '1': #按主题
                childList = cate['childList']
                for list in childList:
                    if list['categoryId'] == 'all':
                        continue
                    self.business.append((list['sort'],list['categoryId'],list['categoryName'],object))
            elif cate['categoryId'] == '3':#按部门
                childList = cate['childList']
                for list in childList:
                    if list['categoryId'] == 'all':
                        continue
                    self.orgList.append((list['sort'],list['categoryId'],list['categoryName'],list['categoryName'],object))
            else:
                continue

    def writeDB(self):
        with MysqlTool() as db:
            # 多条插入
            sql = "INSERT INTO ss_business_list(ID, sort,code,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s,%s)"
            db.execute("delete from ss_business_list")
            for args in self.business:
                db.execute(sql, args, commit=True)

            sql = "INSERT INTO ss_org_list(ID, sort,orgcode,short_name,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s,%s,%s)"
            db.execute("delete from ss_org_list")
            for args in self.orgList:
                db.execute(sql, args, commit=True)

if __name__ == '__main__':
    GetGuide = GetGuide(500109);
    GetGuide.Guide('gr')
    GetGuide.Guide('fr')
    GetGuide.writeDB()
    # 个人主题
    # data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"0","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    # res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10003', headers=headers, data=data, verify=False).json()
    # body = res['C-Response-Body']
    # list1 = json.loads(body)['lIST1']
    # contents = []
    # for list in list1:
    #     contents.append((list['sortcode'],list['typeName'],'gr'))
    # # 法人主题
    # data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"1","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    # res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10003', headers=headers, data=data, verify=False).json()
    # body = res['C-Response-Body']
    # list1 = json.loads(body)['lIST1']
    # for list in list1:
    #     contents.append((list['sortcode'], list['typeName'], 'fr'))
    # print(contents)
    #
    # # 个人部门
    # data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"0","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    # res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10006', headers=headers, data=data,
    #                     verify=False).json()
    # body = res['C-Response-Body']
    # list1 = json.loads(body)['list']
    # orgList = []
    # i=0
    # for list in list1:
    #     i+=1
    #     orgList.append((i,list['orgCode'], list['orgMemo'],list['orgName'], 'gr'))
    # print(orgList)
    # # 法人部门
    # i=0
    # data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"1","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    # res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10006', headers=headers, data=data,
    #                     verify=False).json()
    # list1 = json.loads(res['C-Response-Body'])['list']
    # for list in list1:
    #     i+=1
    #     orgList.append((i,list['orgCode'], list['orgMemo'],list['orgName'], 'fr'))
    # print(orgList)
    # with MysqlTool() as db:
    #     # 多条插入
    #     sql = "INSERT INTO ss_business_list(ID, sort,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s)"
    #     db.execute("delete from ss_business_list")
    #     for args in contents:
    #         db.execute(sql, args, commit=True)
    #
    #     sql = "INSERT INTO ss_org_list(ID, sort,orgcode,short_name,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s,%s,%s)"
    #     db.execute("delete from ss_org_list")
    #     for args in orgList:
    #         db.execute(sql, args, commit=True)