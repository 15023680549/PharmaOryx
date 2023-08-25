from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import csv
import os
import time

dir=os.getcwd()
rows=[]
#存储数据之csv
def tocsv(fileNmae,rows):
    with open(dir+'\\cndrug\\'+fileNmae,'a+', newline='',encoding="utf-8") as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)

def tab0(soup):#国产药品
    # table = soup.find('table')
    # print(table.prettify())
    i = 0
    for tr in table.findAll('tr'):
        if i < 30:
            tds = tr.findAll('td')
            if len(tds) == 0:
                continue
            xh = tds[0].getText()
            pzwh = tds[1].getText()
            ypzwh = tds[2].getText()
            ypbwm = tds[3].getText()
            bwmzs = tds[4].getText()
            cpmc = tds[5].getText()
            ywmc = tds[6].getText()
            spm = tds[7].getText()
            sccj = tds[8].getText()
            scdz = tds[9].getText()
            gg = tds[10].getText()
            jx = tds[11].getText()
            lb = tds[12].getText()
            pzrq = tds[13].getText()
            rows.append([xh, pzwh, ypzwh, ypbwm, bwmzs, cpmc, ywmc, spm, sccj, scdz, gg, jx, lb, pzrq])
            i += 1

def tab1(soup):#注销或撤销国产药
    tables = soup.findAll('table')
    # print(table.prettify())
    table=tables[2]
    i = 0
    for tr in table.findAll('tr'):
        if i < 30:
            tds = tr.findAll('td')
            if len(tds) == 0:
                continue
            xh = tds[0].getText()
            pzwh = tds[1].getText()
            ypzwh = tds[2].getText()
            bz = tds[3].getText()
            cpmc = tds[4].getText()
            ywmc = tds[5].getText()
            spm = tds[6].getText()
            sccj = tds[7].getText()
            scdz = tds[8].getText()
            gg = tds[9].getText()
            jx = tds[10].getText()
            lb = tds[11].getText()
            pzrq = tds[12].getText()
            rows.append([xh, pzwh, ypzwh, bz, cpmc, ywmc, spm, sccj, scdz, gg, jx, lb, pzrq])
            i += 1

def tab_import(soup):#注销或撤销国产药
    tables = soup.findAll('table')
    # print(table.prettify())
    table=tables[4]
    i = 0
    for tr in table.findAll('tr'):
        if i < 30:
            tds = tr.findAll('td')
            if len(tds) == 0:
                continue
            xh = tds[0].getText()
            zczh = tds[1].getText()
            cpmc_cn = tds[2].getText()
            cpmc_en = tds[3].getText()
            spmc_cn = tds[4].getText()
            spmc_en = tds[5].getText()
            jx_cn = tds[6].getText()
            gg_cn = tds[7].getText()
            gzgg_cn = tds[8].getText()
            sccs_cn = tds[9].getText()
            sccs_en = tds[10].getText()
            csgj_cn = tds[11].getText()
            fbzpzwh = tds[12].getText()
            fzrq = tds[13].getText()
            yxjzrq = tds[14].getText()
            fbzqymc = tds[15].getText()
            fbzwhpzrq = tds[16].getText()
            fbzwhyxjzrq = tds[17].getText()
            cplb = tds[18].getText()
            ypbwm = tds[19].getText()
            gsmc_cn = tds[20].getText()
            gsmc_en = tds[21].getText()
            gj_cn = tds[22].getText()
            rows.append([xh, zczh,cpmc_cn,cpmc_en,spmc_cn,spmc_en,jx_cn,gg_cn,gzgg_cn,sccs_cn,sccs_en,csgj_cn,
                         fbzpzwh,fzrq,yxjzrq,fbzqymc,fbzwhpzrq,fbzwhyxjzrq,cplb,ypbwm,gsmc_cn,gsmc_en,gj_cn])
            i += 1

def tab_import_can(soup):#注销或撤销国产药
    tables = soup.findAll('table')
    # print(table.prettify())
    table=tables[6]
    i = 0
    for tr in table.findAll('tr'):
        if i < 30:
            tds = tr.findAll('td')
            if len(tds) == 0:
                continue
            t0 = tds[0].getText()
            t1 = tds[1].getText()
            t2 = tds[2].getText()
            t3 = tds[3].getText()
            t4 = tds[4].getText()
            t5 = tds[5].getText()
            t6 = tds[6].getText()
            t7 = tds[7].getText()
            t8 = tds[8].getText()
            t9 = tds[9].getText()
            t10 = tds[10].getText()
            t11 = tds[11].getText()
            t12 = tds[12].getText()
            t13 = tds[13].getText()
            t14 = tds[14].getText()
            t15 = tds[15].getText()
            t16 = tds[16].getText()
            t17 = tds[17].getText()
            t18 = tds[18].getText()
            t19 = tds[19].getText()
            t20 = tds[20].getText()
            t21 = tds[21].getText()
            t22 = tds[22].getText()
            t23 = tds[23].getText()
            t24 = tds[24].getText()
            t25 = tds[25].getText()
            t26 = tds[26].getText()
            t27 = tds[27].getText()
            t28 = tds[28].getText()
            t29 = tds[29].getText()
            rows.append([t0,t1, t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,
                         t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29])
            i += 1

def par_html(html):
    soup = BeautifulSoup(page_source, 'html.parser')
    # print(soup.prettify())  #格式化输出
    tab_import_can(soup)

if __name__ == '__main__':
    browser=webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')
    browser.get('https://zwykb.cq.gov.cn/qxzz/jjq/fwqd/xzqlqd/')
    page_source=browser.page_source
    # 鼠标点击
    # browser.find_element_by_xpath('/html/body/div[4]/div[5]/div[2]/div[2]/div/div[1]').click()
                                  # '/html/body/div[4]/div[5]/div[2]/div[3]/div/div[1]'
    webdriver.webdriver.common.action_chains.ActionChains(browser).move_to_element(browser.find_element_by_xpath('xxxx')).click().perform()
    #print(page_source)
    # par_html(page_source)
    # tocsv(rows)
    #点击第二页
    # browser.find_element(By.XPATH,'//*[@id="GridViewNational"]/tbody/tr[32]/td/table/tbody/tr/td[2]/a').click()

    # for i in range(1,221):
    #     rows = []
        # browser.find_element(By.XPATH,'//*[@id="GridViewNational"]/tbody/tr[32]/td/table/tbody/tr/td['+str(i)+']/a').click()
        #GridViewNational 国产药品
        #GridViewNationalExpired  国产注销或撤销
        #GridViewImport 进口药
        #GridViewImportExpired 进口药注销或撤销
    #     js = """var theForm = document.forms['form1'];
    #                 theForm = document.form1;
    #                 theForm.__EVENTTARGET.value = 'GridViewImportExpired';
    #                 theForm.__EVENTARGUMENT.value = 'Page$"""+str(i)+"""';
    #                 theForm.submit();"""
    #     browser.execute_script(js)
    #     time.sleep(1)
    #     page_source = browser.page_source
    #     par_html(browser.page_source)
    #     # tocsv('cndrug_import_can.csv',rows)
    # browser.close()