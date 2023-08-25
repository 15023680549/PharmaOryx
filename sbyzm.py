import base64
from PIL import Image
import time
from lxml import etree
from multiprocessing import Pool
import requests
import aiohttp
import asyncio
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
from selenium.webdriver.common.action_chains import ActionChains
import cv2
from selenium.common import exceptions

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

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://zwykb.cq.gov.cn/qxzz/yyxxx/fwqd/xzqlqd/');
    login()
    time.sleep(1)
    #获取总页面
    total = driver.find_element_by_xpath('/html/body/div[4]/div[5]/div[6]/a[6]').text

