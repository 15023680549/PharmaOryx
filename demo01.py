#-*- coding : utf-8-*-
# coding:utf-8
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime, timedelta
import uuid

my_username='root'
my_host='127.0.0.1'
my_password='123456'
my_database='zgdbxt'
# 数据库操作
def ljsql(sql, values,cnx):
    try:
        # 连接到mysql

        # 创建游标对象
        cursor = cnx.cursor()
        # 执行查询并获取所有结果
        cursor.execute(sql, values)
        results = cursor.fetchall()  # 添加这行来读取所有的结果

        cnx.commit()
        # print("********")
        return results  # 返回查询结果（如果有需要的话）
    except mysql.connector.Error as err:
        print(err)
        # break
        return "Error while connecting to MySQL", err
    finally:
        cursor.close()

def banner_time(url_f):
    cnx = mysql.connector.connect(user=my_username, password=my_password, port=3306, host=my_host, database=my_database)
    if url_f == 'http://www.jiangjin.gov.cn/':
        res =requests.get('http://www.jiangjin.gov.cn/')
        soup = BeautifulSoup(res.content, 'html.parser')
        bumen = soup.find('li',id='bumen')
        # print(bumen)
        bumen_dl = bumen.find('dl')
        bumen_a = bumen_dl.findAll('a')
        jiezheng = soup.find('li',id='jiezheng' )
        jiezheng_dl =jiezheng.find('dl')
        jiezheng_a = jiezheng_dl.findAll('a')
        # 获取当前时间
        current_time = datetime.now()
        # 将当前时间格式化为字符串
        time_str = current_time.strftime("%Y%m%d%H%M%S")
        listall = []
        listall_mz =[]
        for list_a in bumen_a:
            a =list_a.get('href')
            mz =list_a.text.strip()
            listall.append(a)
            listall_mz.append(mz)
        for list_a in jiezheng_a:
            a= list_a.get('href')
            mz = list_a.text.strip()
            listall.append(a)
            listall_mz.append(mz)

        i=0
        resyly_jg = ''
        for url in listall:
            if resyly_jg == "true":
                print('0000')
                cnx.close()
                break
            wtlj = url
            uid = uuid.uuid1().hex
            # print(uid)
            ssdw_sql = "SELECT * FROM s_org WHERE NAME = %s"
            ssdw_z = (listall_mz[i],)
            ssdw = ljsql(ssdw_sql,ssdw_z,cnx)[0][0]
            sszb = "2c9430818971470d0189714d0df20014"
            jbjb = 4
            wtcc = 1
            wtlx = 22
            isdel = 0
            szlm = listall_mz[i] + ">首页>部门信息"
            i= i+1
            res = requests.get(url=url)
            soup = BeautifulSoup(res.content, 'html.parser')
            newlist = soup.find('div',class_='newsListWrap')
            # 找到名字
            names = soup.find('div', class_='logoWrap')
            name = names.text.strip()
            banner = newlist.findNext('div').findNext('p').text.strip()
            lasttitle = banner

            banne = newlist.find('ul',class_='listWrap')
            bannes = banne.findAll('li')
            # 获取当前时间
            current_time = datetime.now()
            add_time =current_time
            fxsj = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            # 将当前时间格式化为字符串
            time_str = current_time.strftime("%Y%m%d%H%M%S")
            for ban_text in bannes:
                banner_text = ban_text.text.strip()

                if banner in banner_text:
                    # wtlj = ban_text.find('a').get('href')
                    lasturl = ban_text.find('a').get('href')
                    time = banner_text[-10:]
                    # 将字符串转换为datetime对象
                    date_obj = datetime.strptime(time, "%Y-%m-%d")

                    lastupdatetime = date_obj
                    # 加上14天
                    overdue_date = date_obj + timedelta(days=14)

                    dqsj =overdue_date
                    zgqx = date_obj + timedelta(days=9)
                    dayt = (fxsj - lastupdatetime).days
                    uptimelimt = 14
                    updatelimetname = '2周'
                    if dayt<10:
                        wtms = '正常状态'
                        wtzt = 10
                    elif dayt<14:
                        wtms = '即将逾期'
                        wtzt = 0
                    else:
                        wtms = '严重逾期'
                        wtzt = 0
                        pass
                    print(szlm,wtms,add_time)
                    # 这里做个判断
                    pd_sql =" SELECT * FROM db_question_info WHERE SSDW =%s AND lasttitle=%s AND WTLX=%s AND FXSJ =%s "

                    pd_z = (ssdw,lasttitle,wtlx,fxsj)
                    pd_zt = ljsql(pd_sql,pd_z,cnx)
                    # print(pd_zt)
                    if len(pd_zt)>0:
                        # print('修改')
                        # print('*****')
                        # 修改
                        xg_sql = "UPDATE db_question_info SET KZLJ='',  WTLJ = %s,WTMS=%s,ZGQX=%s,FXSJ=%s,dqsj=%s,ADD_TIME=%s,days=%s,lasttitle=%s,WTZT=%s,lasturl=%s,lastupdatetime=%s,SZLM=%s WHERE ID = %s"
                        xg_nr = (wtlj,wtms,zgqx,fxsj,dqsj,add_time,dayt,lasttitle,wtzt,lasturl,lastupdatetime,szlm,uid,)
                        result_lj =  ljsql(xg_sql,xg_nr,cnx)
                        if len(result_lj) > 0:
                            resyly_jg = 'true'
                            break

                    else:
                        # print('添加')
                        # 添加
                        # print("++++++++++")
                        # print(uid)
                        tj_sql ="INSERT INTO db_question_info (ID,SSDW,SSZB,JBJB,WTCC,WTLX,SZLM,WTLJ,WTMS,ZGQX,FXSJ,dqsj,ADD_TIME,days,uptimelimit,uptimelimitname,lasttitle,isdel,WTZT,lasturl,lastupdatetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        tj_nr =(uid,ssdw,sszb,jbjb,wtcc,wtlx,szlm,wtlj,wtms,zgqx,fxsj,dqsj,add_time,dayt,uptimelimt,updatelimetname,lasttitle,isdel,wtzt,lasturl,lastupdatetime,)
                        result_lj = ljsql(tj_sql,tj_nr,cnx)
                        print(tj_sql)
                        if len(result_lj) > 0:
                            resyly_jg = 'true'
                            break
        cnx.close()
        print('true')
    else:
        # pass
        list_url = []
        res = requests.get('https://www.beibei.gov.cn/')
        soup = BeautifulSoup(res.content, 'html.parser')
        main = soup.select_one('.index-menu>.main')
        uls = main.findAll('ul', class_='clearfix')
        i = 0
        resyly_jg = ''
        for ul in uls:
            if resyly_jg == "true":
                cnx.close()
                break
            lis = ul.findAll('li')
            # print(ul)
            for li in lis:
                i = i + 1
                a = li.find('a').get('href')
                # print(a)
                name = li.find('a').text.strip()
                # lasttitle = name
                uid = uuid.uuid1().hex
                # print(uid)
                ssdw_sql = "SELECT * FROM s_org WHERE NAME = %s"
                ssdw_z = (name)
                ssdw = ljsql(ssdw_sql, [name],cnx)[0][0]
                sszb = "2c9430818971470d0189714d0df20014"
                jbjb = 4
                wtcc = 1
                wtlx = 22
                isdel = 0
                szlm = name+">首页>部门信息"
                res = requests.get(url=a)
                wtlj = a
                soup = BeautifulSoup(res.content, 'html.parser')
                # 获取当前时间
                current_time = datetime.now()
                add_time = current_time
                fxsj = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
                # 将当前时间格式化为字符串
                time_str = current_time.strftime("%Y%m%d%H%M%S")
                now_time = current_time.strftime("%Y-%m-%d")
                time_id = int(time_str)
                try:
                    main = soup.select_one('.main .swiper-slide>a')
                    li_list = soup.select('.head-info ul.infolist>li')
                    lj_url = main.get('href')
                    herf_a = lj_url[0:2]
                    if herf_a == './':
                        banner_url = a + lj_url[2:]
                        lasturl = banner_url
                    else:
                        banner_url = lj_url
                        lasturl = banner_url
                    text = main.find('p').text.strip()
                    lasttitle = text

                    for li in li_list:
                        li_text = li.text.strip()
                        if text in li_text:
                            time = li_text[-10:]
                            # 将字符串转换为datetime对象
                            date_obj = datetime.strptime(time, "%Y-%m-%d")
                            lastupdatetime = date_obj
                            # 加上14天
                            overdue_date = date_obj + timedelta(days=14)
                            dqsj = overdue_date
                            zgqx = date_obj + timedelta(days=9)
                            # 将datetime对象转换回字符串
                            end_date = overdue_date.strftime("%Y-%m-%d")
                            dayt = (fxsj - lastupdatetime).days
                            uptimelimt = 14
                            updatelimetname = '2周'
                            if dayt < 10:
                                wtms = '正常状态'
                                wtzt = 10
                            elif dayt < 14:
                                wtms = '即将逾期'
                                wtzt = 0
                            else:
                                wtms = '严重逾期'
                                wtzt = 0
                                pass
                            print(szlm, wtms, fxsj)
                            # 这里做个判断
                            pd_sql = " SELECT * FROM db_question_info WHERE SSDW =%s AND WTLX=%s "
                            # print(isdel,wtzt,lasturl,lastupdatetime,wtlj)
                            pd_z = (ssdw, wtlx)
                            pd_zt = ljsql(pd_sql, pd_z, cnx)
                            if len(pd_zt) > 0:
                                # 修改
                                uid = pd_zt[0][0]
                                xg_sql = "UPDATE db_question_info SET KZLJ='', WTLJ = %s,WTMS=%s,ZGQX=%s,FXSJ=%s,dqsj=%s,ADD_TIME=%s,days=%s,lasttitle=%s,WTZT=%s,lasturl=%s,lastupdatetime=%s,SZLM=%s WHERE ID = %s"
                                xg_nr = (wtlj, wtms, zgqx, fxsj, dqsj, add_time, dayt, lasttitle, wtzt, lasturl,lastupdatetime, szlm, uid,)
                                result_lj = ljsql(xg_sql, xg_nr, cnx)
                                if len(result_lj) > 0:
                                    resyly_jg = 'true'
                                    break
                            else:
                                # 添加
                                tj_sql = "INSERT INTO db_question_info (ID,SSDW,SSZB,JBJB,WTCC,WTLX,SZLM,WTLJ,WTMS,ZGQX,FXSJ,dqsj,ADD_TIME,days,uptimelimit,uptimelimitname,lasttitle,isdel,WTZT,lasturl,lastupdatetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                tj_nr = (
                                uid, ssdw, sszb, jbjb, wtcc, wtlx, szlm, wtlj, wtms, zgqx, fxsj, dqsj, add_time,
                                dayt, uptimelimt, updatelimetname, lasttitle, isdel, wtzt, lasturl, lastupdatetime,)
                                result_lj = ljsql(tj_sql, tj_nr, cnx)
                                if len(result_lj) > 0:
                                    resyly_jg = 'true'
                                    break
                except:
                    pass

        cnx.close()
        print('true')

a = banner_time('https://www.beibei.gov.cn/')
# a = banner_time('http://www.jiangjin.gov.cn/')
# print(a)




