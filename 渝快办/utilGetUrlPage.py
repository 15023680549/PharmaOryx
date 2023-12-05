#-*- coding : utf-8-*-
# coding:utf-8

import time

from selenium import webdriver

driver = webdriver.Chrome()


#获取url
def geturl(url,xpath):
    #市级行政权力清单，市级公共服务清单
    bszn=['https://zwykb.cq.gov.cn/qxzz/psx/fwqd/xzqlqd/','https://zwykb.cq.gov.cn/qxzz/psx/fwqd/ggfwqd/']
    # for url in bszn:
    driver.get(url);
    time.sleep(1)
    # 获取总页面
    print(url)
    total = int(driver.find_element_by_xpath(xpath).text)
    #退出并关闭浏览器
    driver.quit();
    return total