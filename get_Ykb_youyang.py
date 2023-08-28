#-*- coding : utf-8-*-
# coding:utf-8

from selenium.webdriver.common.action_chains import ActionChains
import cv2
from selenium.common import exceptions
import time
import json
from lxml import etree
from multiprocessing import Pool, Manager
from csv import reader
import aiohttp
import asyncio
import base64
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET
from selenium import webdriver
import pymysql
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

urls=[]
htmls=[]
sem=asyncio.Semaphore(10) #信号量，控制协程数量，防止爬的过快

#是否收费
sfdict = {
    '0':'否',
    '1':'是'
}

#办理形式
blxsdict = {
    '1':'窗口办理',
    '2':'网上办理',
    '3':'快递申请',
    '1^2':'窗口办理,网上办理',
    '1^3':'窗口办理,快递申请',
    '1^2^3':'窗口办理,网上办理,快递申请',
    '2^3':'网上办理,快递申请',
}

#层级
cjdict = {
    '4':'县级'
}
#事项类型字典
sxdict = {
'20':'公共服务',
'10':'其他行政权力',
'09':'行政裁决',
'08':'行政奖励',
'07':'行政确认',
'06':'行政检查',
'05':'行政给付',
'04':'行政征收',
'03':'行政强制',
'02':'行政处罚',
'01':'行政许可'
}
# conn=pymysql.connect(host='',user='',password='',port='',db='',charset='')
# config={
#     'creator':pymysql,
#     'host':"",
#     'port':"3306",
#     'user':"root",
#     'password':"123456",
#     'db':"",
#     'charset':"utf8",
#     'maxconnections':70, #连接池最大连接数
#     'cursorclass':pymysql.cursors.DictCursor
# }
# pool=pymysql(**config)
# conn=pool.connection()
# cursor=conn.cursor()
#
# cursor.execute("SELECT VERSION()")
#
# cursor.close()
# conn.close()
# print('链接数据库成功!')
# cursor=conn.cursor()

#存储数据之csv
def tocsv(fileNmae,rows):
    with open('E:\\work\\djrm\\ykb\\'+fileNmae,'a+', newline='',encoding="utf-8-sig") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def readurl(fileNmae):
    with open('E:\\work\\djrm\\ykb\\'+fileNmae,'r',encoding='gbk') as f:
        csv_reader=reader(f)
        list_of_rows=list(csv_reader)
        for i in range(0,len(list_of_rows)):
            urls.append(list_of_rows[i])

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
                htmls.append([html['C-Response-Body'],url[2]])
                name=json.loads(html['C-Response-Body'])
                print('异步获取%s.'% name['name'],url[2])

#协程调用，请求网页
def main_get_html():
    loop=asyncio.get_event_loop()   #获取事件循环
    tasks=[get_html(url) for url in urls]   #把所有任务放入一个列表中
    loop.run_until_complete(asyncio.wait(tasks))    #激活协程

def parse(html):
    url = html[1]
    html = json.loads(html[0])
    # 获取内容
    name = html["name"]  # 事项名称
    stype = sxdict[html["type"]]  # 事项类型
    orgname = html['orgName']  # 实施主体
    exeLevel = html['exeLevel']  # 行使层级 4 县级
    legalFileName = html['legalFileName']  # 设定依据
    handleForm = html['handleForm']  # 办理形式
    isCharge = html['isCharge']  # 是否收费 0否
    collectionType = html['collectionType']  # 征收种类
    matterFileList = html['matterFileList']  # 申请材料
    fname = ''  # 申请材料
    if(matterFileList!=None):
        for emp in matterFileList:
            fname = ',' + emp['fileName']
        fname=fname[1:]
    # 写入csv文件
    # str='事项类型<br />'+stype+',实施主体<br />'+orgname+',行使层级</br>'+exeLevel+',办理形式</br>'+handleForm+',是否收费</br>'+isCharge+',征收种类</br>'+collectionType+',设定依据</br>'+legalFileName+',申请材料</br>'+fname
    str = '事项类型<br />' + stype + ',实施主体<br />' + orgname
    if (exeLevel != None):
        str = str + ',行使层级</br>' + cjdict[exeLevel]
    if (handleForm != None):
        str = str + ',办理形式</br>' + blxsdict[handleForm]
    if(isCharge!=None):
        str=str+',是否收费</br>' + sfdict[isCharge]
    if (legalFileName != None):
        str = str + ',设定依据</br>' + legalFileName
    if (collectionType != None):
        str = str + ',征收种类</br>' + collectionType
    if (fname != ''):
        str = str + ',申请材料</br>' + fname
    return [name, url, stype, str]

#使用多进程解析html
def multi_parse_html(html,cnt,rows):
    try:
        list = parse(html)
    except Exception as ex:
        print(ex,html[0])
    rows.append(list)
    print('第%d个html-----------date:%s'% (cnt,time.time()))

#多进程调用总函数，解析html
def main_parse_html(rows):
    p=Pool(2)
    i=0
    for html in htmls:
        i+=1
        p.apply_async(multi_parse_html,args=(html,i,rows))
    p.close()
    p.join()

#判断元素是否存在
def iselement():
    """
    基本实现判断元素是否存在
    :param browser: 浏览器对象
    :param xpaths: xpaths表达式
    :return: 是否存在
    """
    try:
        driver.find_element_by_class_name('ui-dialog-body')
        return True
    except exceptions.NoSuchElementException:
        return False

#验证
def yz():
    # 计算滑动位置
    jl = identify_gap('bg.png', 'bg1.png', 'out.png')
    # 滑块
    more_files_ele = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[3]/div[2]/div[2]/div")
    action = ActionChains(driver)
    action.move_to_element_with_offset(more_files_ele, jl, 0)
    action.click_and_hold(more_files_ele).perform()
    action.move_by_offset(jl + 10, 0).perform()
    action.release()
    time.sleep(0.2)
    #点击登录
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[5]/button').click()

#下载图片
def download_img(filename,js):
    base64str = driver.execute_script(js)
    resultstr = base64str.strip("data:image/png;base64")
    resultstr = resultstr[1:]
    imagedata = base64.b64decode(resultstr)
    file = open(filename, "wb")
    file.write(imagedata)
    file.close()

#下载背景图和滑块图片
def download_yzm():
    more_files_ele = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[3]/div[2]/div[2]/div")
    action = ActionChains(driver)
    action.move_to_element(more_files_ele)
    action.click(more_files_ele)
    action.perform()
    action.release()
    time.sleep(0.2)
    js = '''return document.getElementsByTagName('canvas')[0].toDataURL()'''
    filename='./bg.png'
    download_img(filename,js)
    js = '''return document.getElementsByTagName('canvas')[1].toDataURL()'''
    filename = './bg1.png'
    download_img(filename,js)

def identify_gap(bg, tp, out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 10, 10)
    tp_edge = cv2.Canny(tp_img, 50, 80)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, bg_img)  # 保存在本地
    # 返回缺口的X坐标
    return tl[0]

#登录
def login():
    # 登录页面
    driver.find_element_by_xpath('/html/body/div[3]/div[1]/ul/li[4]/div/div[2]').click()
    time.sleep(1)
    # 点击关闭按钮
    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button').click()
    driver.find_element_by_id('username').send_keys('15023680549')
    driver.find_element_by_id('password').send_keys('19920211.jY')
    while(True):
        # 下载验证滑块图片 一直滑动到登录上为止
        download_yzm()
        #滑动验证
        yz()
        #判断元素是否存在
        istc = iselement()
        if(istc==False):
            break

#展开折叠
def unfold():
    for i in range(1, 11):
        time.sleep(0.2)
        xpath = '/html/body/div[4]/div[5]/div[2]/div[' + str(i) + ']/div/div[1]'
        # driver.find_element_by_xpath(xpath).click()
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        webdriver.ActionChains(driver).move_to_element(element).click().perform()

#获取折叠内容 url,id,title
def getContent(filename):
    for link in driver.find_elements_by_class_name('sx-zn'):
        href = 'https://zwykb.cq.gov.cn/qxzz/yyxxx/' + link.get_attribute('_href').replace('../../', '')
        businessid = link.get_attribute('businessid')
        title = link.get_attribute('keywords')
        row = [title, businessid, href]
        tocsv(filename, [row])

#获取url
def geturl(filename):
    login()
    time.sleep(1)
    # 获取总页面
    total = int(driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[6]/a[6]').text)
    j = 2
    while (True):
        j += 1
        print(j)
        # 展开页面的折叠
        unfold()
        time.sleep(1)
        # 获取页面title,url及id
        getContent(filename)
        # 下一页
        # driver.find_element_by_class_name('yj-pga8').click()
        # 改为通过调用js
        js = 'getDataList(' + str(j) + ',10)'
        driver.execute_script(js)
        time.sleep(2)
        if (j == total):
            break

if __name__ == '__main__':
    fileName='酉阳url.csv'
    # 通过登录获取服务清单title,url,id等信息
    # driver = webdriver.Chrome()
    # driver.get('https://zwykb.cq.gov.cn/qxzz/yyxxx/fwqd/xzqlqd/');
    # geturl(fileName)

    #读取存储url csv到数组中
    readurl(fileName)
    #定义多进程共享变量
    manager = Manager()
    rows = manager.list()
    main_get_html()
    main_parse_html(rows)
    tocsv('酉阳body.csv', rows)