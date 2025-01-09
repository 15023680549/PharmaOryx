# -*- coding : utf-8-*-
# coding:utf-8
import guide.utilFile as MyFileTool
from guide.utilFile import UtilFile
from multiprocessing import Pool, Manager
import threading
import aiohttp_socks
import os
import json
import aiohttp
import asyncio
import time
from scripts.utilDict import YkbDict


class MyGetHtmlTool:
    def __init__(self, urls):
        # 修改事件循环的策略，不能放在协程函数内部，这条语句要先执行
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        self.htmls = []
        self.urls = urls
        self.rows = []
        self.sem = asyncio.Semaphore(10)  # 信号量，控制协程数量，防止爬的过快
        self.proxies={'https':'https://218.87.205.54:22455'}

    # 获取请求json
    async def get_html(self, url):
        async with self.sem:
            # proxies = "http://127.0.0.1:10809"
            # proxies = "http://115.223.11.212:50000"
            # connector = aiohttp_socks.ProxyConnector.from_url(proxies)
            # async with aiohttp.ClientSession(connector=connector,headers=self.headers) as session:  # 获取session
            async with aiohttp.ClientSession(headers=self.headers) as session:  # 获取session
                # async with session.get('https://cqykb.cq.gov.cn/pc/xindian/item_guid/guid_detail?rowGuid='+url.split('=')[1]) as resp:  # 提出请求
                async with session.get('https://cqykb.cq.gov.cn/pc/xindian/item_guid/guid_detail?rowGuid='+url[1]) as resp:  # 提出请求
                    html = await resp.json()  # 直接获取到bytes
                    self.htmls.append([html['data'], url[2]])
                    print(f'异步获取 {url[0]}, {url[2]}')
                    # self.htmls.append([html['data'], url])
                    # print(f'异步获取 {url}, {url}')

    # 协程，批量请求链接
    def main_get_html(self):
        loop = asyncio.get_event_loop()  # 获取事件循环
        tasks = [self.get_html(url) for url in self.urls]  # 把所有任务放入一个列表中
        loop.run_until_complete(asyncio.wait(tasks))  # 激活协程

    # 多线程，解析html结果
    # def main_parse_html(self,rows):
    #     threads = []
    #     for i, html in enumerate(self.htmls):
    #         t = threading.Thread(target=self.multi_parse_html, args=(html, i + 1, rows))
    #         threads.append(t)
    #         t.start()
    #     for t in threads:
    #         t.join()

    # pool方法都使用了queue.Queue将task传递给工作进程。multiprocessing必须将数据序列化以在进程间传递。方法只有在模块的顶层时才能被序列化，跟类绑定的方法不能被序列化，就会出现上面的异常。
    def main_parse_html(self,rows):
        for i, html in enumerate(self.htmls):
            self.multi_parse_html(html, i + 1, rows)
        # try:
        #     with Pool(2) as p:
        #         for i, html in enumerate(self.htmls):
        #             p.apply_async(self.multi_parse_html, args=(html, i + 1, rows))
        #         p.close()
        #         p.join()
        # except Exception as ex:
        #     print(ex)

    # 多进程调用总函数，解析html
    def main_parse_htmlText(self):
        p = Pool(2)
        for i,html in enumerate(self.htmls):
            p.apply_async(self.multi_parse_htmlToText, args=(html, i+1))
            # p.apply_async(self.multi_parse_html, args=(html, i+1))
        p.close()
        p.join()

    def whilePauseToText(self):
        for i, html in enumerate(self.htmls):
            print(f'第 {i} 个 html:{html[1]} date: {time.time()}')
            self.util_parse_htmlToText(html,i)

    def multi_parse_htmlToText(self, html, cnt):
        try:
            print(f'第 {cnt} 个 html ----------- date: {time.time()}')
            # self.main_parse_html(html)  #函数
            self.main_parse_htmlToText(html)  #函数
        except Exception as e:
            error_info = f'Error in parsing HTML {html[1]}: {str(e)}'
            print(error_info)

    def multi_parse_html(self, html, cnt, rows):
        try:
            print(f'第 {cnt} 个 html ----------- date: {time.time()}')
            parsed_list = self.util_parse_html(html)  # 返回解析后的数据
            rows.append(parsed_list)
        except Exception as e:
            error_info = f'Error in parsing HTML {html[1]}: {str(e)}'
            rows.append(error_info)  # 记录错误信息
            print(error_info)

    def util_parse_html(self, html):
        str = ''
        # 这里是解析 HTML 的逻辑，返回解析后的数据
        # '<strong>对集体商标注册人的成员发生变化，注册人未向商标局申请变更注册事项的处罚</strong><br/><strong>办理主体:</strong>重庆市北碚区市场监督管理局<br/><strong>法定办结时限:</strong>0天  <strong>咨询方式:</strong>咨询电话：023-81912121  <strong>监督投诉方式:</strong>投诉电话：023-81912117<br/>'
        url = html[1]
        guidDetail = html[0]['guidDetail']
        taskName = guidDetail['taskName']
        staskName = '<strong>'+guidDetail['taskName']+'</strong><br>'
        str += staskName
        orgId = guidDetail['orgId']
        deptName = guidDetail['deptName'] #办理主体
        str += '<strong>办理主体:</strong>'+deptName+'<br>'
        anticipateDay = guidDetail['anticipateDay'] #法定办结时限
        promiseDay = guidDetail['promiseDay'] #承诺办结时限
        lobbys = html[0]['lobbys'] #办理地址
        linkWay = guidDetail['linkWay'] #咨询方式
        str += '<strong>咨询方式:</strong>'+linkWay+'<br>'
        superviseWay = guidDetail['superviseWay'] #监督投诉方式
        str += '<strong>监督投诉方式:</strong>'+superviseWay+'<br>'
        taskType = guidDetail['taskType'] #事项类型
        sxlx = YkbDict.sxdictName[taskType]
        serveType = guidDetail['serveType'] #服务对象
        dx = ''
        if serveType != None and serveType!='':
            for fwdx in serveType.split(','):
                dx += ' ' + YkbDict.serviceObjectName[fwdx]
                if fwdx == 7 or fwdx == 8:
                    print(url)
            str += '<strong>服务对象:</strong>' + dx + '<br/>'

        naturalThemeType = guidDetail['naturalThemeType'] #面向自然人主题
        legalThemeType = guidDetail['legalThemeType'] #面向法人主题
        if naturalThemeType==None:
            zrr=''
        else:
            zrr = naturalThemeType  # 自然人
        if legalThemeType==None:
            fr=''
        else:
            fr = legalThemeType  # 法人

        serveType = guidDetail['serveType'] #服务对象
        isFee = guidDetail['isFee'] #是否收费
        for lobby in lobbys:
            lobby['address'] #窗口地址
            lobby['tel'] #窗口电话
            lobby['time'] #办理时间
            lobby['timeDelayBus'] #交通指引
        return [taskName,url,sxlx,str,deptName,orgId,dx,'\t'+zrr,'\t'+fr]  # 返回一个列表

        def util_down_material(self):
            None

        def main_parse_htmlToText(self,rows):
            threads = []
            for i, html in enumerate(self.htmls):
                t = threading.Thread(target=self.util_parse_htmlToText, args=(html, i + 1, rows))
                threads.append(t)
            t.start()
            for t in threads:
                t.join()

    def util_parse_htmlToText(self, html,i):
        # try:
            str = ''
            # 这里是解析 HTML 的逻辑，返回解析后的数据
            url = html[1]
            if html[0]==None:
                return
            if 'guidDetail' not in html[0] or html[0]['guidDetail']==None:
                return
            guidDetail = html[0]['guidDetail']
            taskName = guidDetail['taskName']
            # 先判断文件是否存在,如果存在就不重复写入
            fileName = f'{taskName}.txt'.replace('/', '')
            if os.path.exists(f'text\\{fileName}'):
                print(f'{fileName} 文件已存在')
                return

            str += f'事项名称:'+taskName+'\n'
            str +=f'到现场次数:{guidDetail["limitSceneNum"]}次,法定办结时限:{guidDetail["anticipateDay"]}个工作日,承诺办结时限:{guidDetail["promiseDay"]}个工作日'+'\n'
            # str +=f'办事服务：0星，办事指南：0星'+'\n\n'

            str +=f'{taskName}-基本信息'+'\n'
            #str +='办事信息'+'\n'
            serveType = guidDetail['serveType']  # 服务对象
            dx = ''
            if serveType != None and serveType != '':
                for fwdx in serveType.split(','):
                    dx += ' ' + YkbDict.serviceObjectName[fwdx]
                    if fwdx == 7 or fwdx == 8:
                        print(url)
            sxlx = YkbDict.sxdictName[guidDetail['taskType']]# 事项类型
            str +='实施主体：'+guidDetail['deptName']+'，服务对象：'+dx+'，事项类型：'+sxlx+'\n'
            blxs=''
            handleType = guidDetail['handleType']
            if handleType!=None:
                for xs in guidDetail['handleType'].split(','):
                    blxs +=YkbDict.blxsdict[xs]+' '
            str += '办理形式：'+blxs+'，办件类型：即办件\n'
            str += f'咨询方式：'+guidDetail['linkWay']+'监督投诉方式：'+guidDetail['superviseWay']+'\n'

            #str += '结果信息\n'
            #以下为下载链接
            # imgUrl = f'https://cqykb.cq.gov.cn/pc/xindian/item_guid/get_attach_info?cliengguid={guidDetail["resultGuid"]}&isOnline=false'
            # file = UtilFile.DownloadFile('','images',imgUrl) #请求审批结果样本
            if 'resultList' in guidDetail and guidDetail['resultList']!=None:
                resultList = json.loads(guidDetail['resultList']) #审批结果
                file =''
                if resultList!=None:
                    for res in resultList:
                        file+=res['ATTACHFILENAME']+' '
                resultType=''
                if guidDetail['resultType']!=None:
                    for rst in guidDetail['resultType'].split(','):
                        resultType+=YkbDict.spjglxDictName[rst]+' '
                resultName=''
                if guidDetail['resultName']!=None:
                    resultName = guidDetail['resultName']
                str += '审批结果名称：'+resultName+'，审批结果样本：'+file+'，审批结果类型：'+resultType+'\n'

            #str += '收费信息\n'
            if guidDetail['isFee']!=None:
                isFee=YkbDict.sfdict[guidDetail['isFee']]
                str+=f'是否收费：{isFee},'
            if guidDetail['isPayOnline'] != None:
                isPayOnline = YkbDict.sfdict[guidDetail['isPayOnline']]
                str += f'是否支持网上支付：{isPayOnline}\n'

            #str += '审批信息\n'
            if guidDetail["itemSource"]!=None:
                itemSource=YkbDict.qllyDictName[guidDetail["itemSource"]]
                str +=f'权力来源：{itemSource}，'
            if guidDetail["useLevel"]!=None:
                useLevel=YkbDict.cjdictName[guidDetail["useLevel"]]
                str += f'行使层级：{useLevel}，'
            if guidDetail["deptType"] != None:
                deptType=YkbDict.ssztDictName[guidDetail["deptType"]]
                str += f'实施主体性质：{deptType}'
            str +='\n'

            #str += '送达信息\n'
            if guidDetail['isExpress']!=None:
                isExpress=YkbDict.sfdict[guidDetail['isExpress']]
                str += f'是否支持物流快递：{isExpress},'
            #str += '中介服务信息\n'
            str += f'中介服务：{guidDetail["serviceType"]}\n'

            #办理深度
            wsblsd=''
            #print(guidDetail['wsfwsd'])
            if guidDetail['wsfwsd']!=None:
                for sd in guidDetail['wsfwsd'].split(','):
                    wsblsd += YkbDict.sdDictName[sd] + ' '
            #其它信息
            str += f'{taskName}-其他信息\n'
            str += f'基本编码：{guidDetail["catalogCode"]}，实施编码:{guidDetail["taskCode"]},网上办理深度：{wsblsd}\n'
            isSchedule=''
            if guidDetail['isSchedule']!=None:
                isSchedule=YkbDict.sfdict[guidDetail['isSchedule']]
            onlineCheck=''
            if guidDetail['onlineCheck'] != None:
                onlineCheck = YkbDict.sfdict[guidDetail['onlineCheck']]
            str +=f'必须现场办理原因：{guidDetail["sceneReason"]}，是否支持预约办理：{isSchedule}，是否网办：{onlineCheck}\n'
            zrr=''
            fr=''
            if guidDetail["naturalThemeType"]!=None:
                for zr in guidDetail["naturalThemeType"].split(','):
                    zrr = YkbDict.grzt[zr]+' '
            if guidDetail["legalThemeType"]!=None:
                for f in guidDetail["legalThemeType"].split(','):
                    fr = YkbDict.frzt[f]+' '
            str +=f'面向自然人主题分类：{zrr},面向法人主题分类：{fr}，实施主体编码：'+guidDetail['deptCode']+'\n'
            str +=f'法定办结时限说明：{guidDetail["anticipateState"]}，承诺办结时限说明：{guidDetail["promiseState"]}\n'

            str += '########################################################\n'
            #受理条件
            itemConditions=html[0]['itemConditions'] #受理条件
            if itemConditions!=None and len(itemConditions)>0:
                str +=f'{taskName}-受理条件\n'
                for condition in itemConditions:
                    str +='条件类型：'+YkbDict.sltjDict[condition['conditionType']]+'\n'
                    str +='条件名称：'+condition['conditionName']+'\n'
                    str +='适用类型：'+condition['conditionSituation']+'\n'
                str += '########################################################\n'

            #材料清单
            clqd=''
            if 'itemMaterials' in html[0] and html[0]['itemMaterials']!=None:
                itemMaterials=html[0]['itemMaterials']
                if itemMaterials!=None:
                    for material in html[0]['itemMaterials']:
                        clqd +=f'材料名称：{material["materialName"]}，材料类型：{YkbDict.clDictName[material["materialType"]]}，来源渠道及说明：{material["source_explain"]})，材料要求：形式:{YkbDict.zzhdzbDictName[material["zzhdzb"]]},材料必要性:{YkbDict.clbyxName[material["need"]]}\n'
            else:
                matterId = UtilFile.getMatterId('',html[0]['onlineUrl'],html[0]['materialUrl'])
                if matterId!='1111254491906':
                    clqd += UtilFile.getQuestByMatterId('',matterId)
            if len(clqd)>0:
                str += f'{taskName}-材料清单\n'
                str += '办理该事项所需的材料清单如下：\n'
                str += clqd
                str += '########################################################\n'

            #办理地点
            lobbys = html[0]['lobbys']
            if lobbys!=None and len(lobbys)>0:
                str +=f'{taskName}-办理地点\n'
                for lobby in lobbys:
                    str +=f'窗口地址:{lobby["address"]}\n'
                    str +=f'窗口电话:{lobby["tel"]}\n'
                    str +=f'办理时间:{lobby["time"]}\n'
                    str +=f'交通指引:{lobby["timeDelayBus"]}\n'
                str += '########################################################\n'

            #设定依据
            byLaws = html[0]['byLaws']
            if byLaws!=None and len(byLaws)>0:
                str +=f'{taskName}-设定依据\n'
                for byLaw in byLaws:
                    str +=f'法律法规名称:{byLaw["lawName"]}\n'
                    str +=f'依据文号:{byLaw["accordingNumber"]}\n'
                    str +=f'条款号:{byLaw["termsNumber"]}\n'
                    str +=f'条款内容:{byLaw["termsContent"]}\n'
                str += '########################################################\n'

            #办理流程
            activitys = html[0]['activitys']
            if activitys!=None and len(activitys)>0:
                str+=f'{taskName}-办理流程\n'
                for activity in activitys:
                    if activity["activityName"]=='颁证':
                        str += f'    {activity["orderNumber"]}{activity["activityName"]}\n'
                        str +=f'送达方式：'+activity["type"]+'\n'
                        str +=f'颁发证件：'+activity['send']+'\n'
                        str +=f'办理期限：{activity["handleTimeLimit"]}个工作日\n'
                    else:
                        str += f'    {activity["orderNumber"]}{activity["activityName"]}\n'
                        str += f'审查标准:{activity["standard"]}\n'
                        str += f'审查结果:{activity["result"]}\n'
                        str += f'完成时限:{activity["handleTimeLimit"]}个工作日\n'
                str += '########################################################\n'

            #收费项目
            charges = html[0]['charges']
            if charges!=None and len(charges)>0:
                str +=f'{taskName}-收费项目\n'
                for charge in charges:
                    str +=f'序号:{charge["orderNum"]}，收费项目名称：{charge["feeName"]}，收费标准：{charge["feeStand"]}，收费依据：{charge["byLaw"]}，是否允许减免：{YkbDict.isTrue[charge["isDesc"]]}，允许减免依据：{charge["descLaw"]}，备注：{charge["remark"]}\n'
                str+='########################################################\n'

            #常见问题
            itemQAs = html[0]['itemQAs']
            if itemQAs!=None and len(itemQAs)>0:
                str +=f'{taskName}-常见问题\n'
                for itemQA in itemQAs:
                    str +=f'Q:{itemQA["question"]}\n'
                    str +=f'A:{itemQA["answer"]}\n'
                str += '########################################################\n'

            str +=f'{taskName}-来源于：'+html[1]
            str = str.replace('None','-')
            #文件名称
            # fileName = f'{taskName}.txt'
            MyFileTool.toText('text',fileName,str,'w+')
        # except Exception as ex:
        #     print(html)
        #     print(ex)



# 示例使用
if __name__ == "__main__":
    urls = [['对就业困难人员（含建档立卡贫困劳动力）实施就业援助中的职业介绍补贴申领','5281e12f-e2cc-4529-9647-1e189bedaa05','https://zwykb.cq.gov.cn/qxzz/bbq/bszn/?rowGuid=5281e12f-e2cc-4529-9647-1e189bedaa05'],
            ['参保单位注销','993d9ae1-8231-4dff-8ff0-0a3601a29720','https://zwykb.cq.gov.cn/qxzz/bbq/bszn/?rowGuid=993d9ae1-8231-4dff-8ff0-0a3601a29720'],
            ['企业社会保险登记','6796fc9f-689e-45bf-9327-4c2c3c21804e','https://zwykb.cq.gov.cn/qxzz/bbq/bszn/?rowGuid=6796fc9f-689e-45bf-9327-4c2c3c21804e&itemId=1203df22-0629-4b90-8cf8-5735eecc1506']]
    tool = MyGetHtmlTool(urls)
    #使用 Manager 来管理进程间共享的列表
    with Manager() as manager:
        rows = manager.list()
    #     # tool.main_get_html()  # 获取 HTML
    #     #tool.main_parse_html(rows)  # 解析 HTML
    #     #rows = tool.main_get_html(html)
        tool.main_get_html()  # 获取 HTML
    #     # tool.main_parse_html(rows)  # 解析 HTML
        for html in tool.htmls:
            tool.util_parse_htmlToText(html,1)
        # print(rows)
    # 输出结果
    #     for row in rows:
    #         print(row)
    # MyFileTool.tocsv('aa.csv',rows,'w+')