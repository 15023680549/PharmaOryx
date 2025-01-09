#-*- coding : utf-8-*-
# coding:utf-8
import os
from csv import reader
from selenium import webdriver
import scripts.utilParseHtml as utilParseHtml
from scripts.utilMysql import MysqlTool
import requests
import csv
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

orgcode='500109'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

def putMsql():
    None

if __name__ == '__main__':
    # 个人主题
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"0","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10003', headers=headers, data=data, verify=False).json()
    body = res['C-Response-Body']
    list1 = json.loads(body)['lIST1']
    contents = []
    for list in list1:
        contents.append((list['sortcode'],list['typeName'],'gr'))
    # 法人主题
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"1","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10003', headers=headers, data=data, verify=False).json()
    body = res['C-Response-Body']
    list1 = json.loads(body)['lIST1']
    for list in list1:
        contents.append((list['sortcode'], list['typeName'], 'fr'))
    print(contents)

    # 个人部门
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"0","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10006', headers=headers, data=data,
                        verify=False).json()
    body = res['C-Response-Body']
    list1 = json.loads(body)['list']
    orgList = []
    i=0
    for list in list1:
        i+=1
        orgList.append((i,list['orgCode'], list['orgMemo'],list['orgName'], 'gr'))
    print(orgList)
    # 法人部门
    i=0
    data = '{"txnCommCom":{"txnIttChnlId":"C0071234567890987654321","txnIttChnlCgyCode":"BC01C101"},"txnBodyCom":{"regnCode":"500109","serviceObject":"1","addrLvlCd":"3","type":"30","isLinkMatter":"1"}}'
    res = requests.post('https://ykbapp.cq.gov.cn:8082/gml/web10006', headers=headers, data=data,
                        verify=False).json()
    list1 = json.loads(res['C-Response-Body'])['list']
    for list in list1:
        i+=1
        orgList.append((i,list['orgCode'], list['orgMemo'],list['orgName'], 'fr'))
    print(orgList)
    with MysqlTool() as db:
        # 多条插入
        sql = "INSERT INTO ss_business_list(ID, sort,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s)"
        db.execute("delete from ss_business_list")
        for args in contents:
            db.execute(sql, args, commit=True)

        sql = "INSERT INTO ss_org_list(ID, sort,orgcode,short_name,name,class_type) VALUES (replace(UUID(),'-',''),%s,%s,%s,%s,%s)"
        db.execute("delete from ss_org_list")
        for args in orgList:
            db.execute(sql, args, commit=True)