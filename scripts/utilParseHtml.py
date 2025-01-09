#-*- coding : utf-8-*-
# coding:utf-8

import json
import scripts.utilDict as utilDict

#取渝快办详细数据(json)

def parse(html):
    url = html[1]
    html = json.loads(html[0])

    orgname = html['orgName']  # 实施主体
    org = html['orgCode']  # 部门编码
    serviceObject=html['serviceObject']#服务对象
    legalDay = html['legalDay'] #法定办结时限
    promiseDay = html['promiseDay'] #承诺办结时限
    workAddress = html['workAddress'] #主体，办理地点，窗口电话
    workTime = html['workTime']#办理时间和交通指引
    adviceWay = html['adviceWay'] #咨询方式
    superviseWay = html['superviseWay'] #监督投诉电话
    handleForm = html['handleForm'] #办理形式
    name = html["name"]  # 事项名称
    stype = utilDict.sxdictName[html["type"]]  # 事项类型
    exeLevel = html['exeLevel']  # 行使层级 4 县级
    legalFileName = html['legalFileName']  # 设定依据
    isCharge = html['isCharge']  # 是否收费 0否
    matterFileList = html['matterFileList']  # 申请材料
    classificationInfos = html['classificationInfos']  # 面向法人主题自然人法人主题
    zrr = '' #自然人
    fr = '' #法人
    if(classificationInfos!=None):
        for ifca in classificationInfos:
            if ifca['serviceObject']=='0':
                zrr =',' + ifca['typename']
            if ifca['serviceObject']=='1':
                fr =',' + ifca['typename']
    if len(zrr)>0:
        zrr=zrr[1:]
    if len(fr) > 0:
        fr = fr[1:]

    fname = ''  # 申请材料
    if(matterFileList!=None):
        for emp in matterFileList:
            fname = ',' + emp['fileName']
        fname=fname[1:]
    # 写入csv文件
    # 获取内容，事项名称
    if name!=None:
        str = '<strong>' + name + '</strong><br/>' #事项名称
    #办理主体
    if orgname!=None:
        str = str+'<strong>办理主体:</strong>'+orgname+'<br/>'
    # 服务对象
    dx = ''
    if serviceObject!=None:
        for fwdx in serviceObject.split('^'):
            dx = dx + ' ' + utilDict.serviceObjectName[fwdx]
            if fwdx==7 or fwdx==8:
                print(url)
        str = str + '<strong>服务对象:</strong>' + dx + '<br/>'
    #申请材料
    if fname!='':
        str = str + '<strong>申请材料:</strong>' + fname + '<br/>'
    #法定办结时限
    if legalDay!=None and legalDay!='null':
        str = str+'<strong>法定办结时限:</strong>'+legalDay+'天  '
    #承诺办结时限
    if promiseDay!=None and promiseDay!='null':
        str = str+'<strong>承诺办结时限:</strong>'+promiseDay+'天<br/>'
    #办理地点
    if workAddress!=None:
        str = str+'<strong>办理地点:</strong>'+workAddress.split('^')[1]+'<br/>'
        str = str+'<strong>窗口电话:</strong>'+workAddress.split('^')[2]+'<br/>'
    #办理时间
    if workTime!=None:
        str = str+'<strong>办理时间:</strong>'+workTime.split('^')[0]+'<br/>'
        str = str+'<strong>交通指引:</strong>'+workTime.split('^')[1]+'<br/>'
    # 咨询方式
    if adviceWay!=None:
        str = str + '<strong>咨询方式:</strong>' + adviceWay + '  '
    # 监督投诉方式
    if superviseWay!=None:
        str = str + '<strong>监督投诉方式:</strong>' + superviseWay + '<br/>'
    #办理形式
    if (handleForm != None):
        blxs = ''
        for xs in handleForm.split('^'):
            blxs = blxs+' '+utilDict.blxsdict[xs]
        str = str + '<strong>办理形式:</strong>' + blxs + '<br/>'
    #是否收费
    if isCharge!=None:
        str = str + '<strong>是否收费:</strong>' + utilDict.sfdict[isCharge] + '<br/>'
    return [name, url, stype, str, orgname,org,dx,zrr,fr]