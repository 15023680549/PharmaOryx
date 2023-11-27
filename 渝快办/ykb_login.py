#-*- coding : utf-8-*-
# coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import base64
import cv2

class ykbLogin():
    #初始化
    def __init__(self, driver):
        self.driver = driver

    #下载背景图和滑块图片
    def download_yzm(self):
        more_files_ele = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[3]/div[2]/div[2]/div")
        action = ActionChains(self.driver)
        action.move_to_element(more_files_ele)
        action.click(more_files_ele)
        action.perform()
        action.release()
        time.sleep(0.2)
        js = '''return document.getElementsByTagName('canvas')[0].toDataURL()'''
        filename= '../bg.png'
        ykbLogin.download_img(filename,js)
        js = '''return document.getElementsByTagName('canvas')[1].toDataURL()'''
        filename = '../bg1.png'
        ykbLogin.download_img(filename,js)

    # 验证
    def yz(self):
        # 计算滑动位置
        jl = ykbLogin.identify_gap('bg.png', 'bg1.png', 'out.png')
        # 滑块
        more_files_ele = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[3]/div[2]/div[2]/div")
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(more_files_ele, jl, 0)
        action.click_and_hold(more_files_ele).perform()
        action.move_by_offset(jl + 10, 0).perform()
        action.release()
        time.sleep(0.2)
        # 点击登录
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[1]/form/div[5]/button').click()

    #下载图片
    def download_img(self,filename,js):
        base64str = self.driver.execute_script(js)
        resultstr = base64str.strip("data:image/png;base64")
        resultstr = resultstr[1:]
        imagedata = base64.b64decode(resultstr)
        file = open(filename, "wb")
        file.write(imagedata)
        file.close()

    def identify_gap(self,bg, tp, out):
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
    def login(self):
        # 登录页面
        self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[1]/div[2]').click()
        time.sleep(1)
        # 点击关闭按钮
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button').click()
        self.driver.find_element_by_id('username').send_keys('15023680549')
        self.driver.find_element_by_id('password').send_keys('19920211.jY')
        while(True):
            # 下载验证滑块图片 一直滑动到登录上为止
            ykbLogin.download_yzm()
            #滑动验证
            ykbLogin.yz()
            #判断元素是否存在
            istc = ykbLogin.iselement()
            if(istc==False):
                break