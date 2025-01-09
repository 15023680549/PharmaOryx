from bs4 import BeautifulSoup
import requests
from weixin import Weixin
from flask import Flask, jsonify, request, url_for


headers={
    'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x1800312d) NetType/WIFI Language/zh_CN'
}
url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9b429af89628085&redirect_uri=https%3A%2F%2Fwxauth1.npoll.net%2Fwxauth%2Fcallback%3Fredirect%3DaHR0cHM6Ly9kdmx3Nmgud3gubnBvbGwubmV0L2FjdD9hY3Q9MjIzOTQ4&response_type=code&scope=snsapi_userinfo&state=&connect_redirect=1#wechat_redirect'
# res = requests.get('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9b429af89628085&redirect_uri=https%3A%2F%2Fwxauth1.npoll.net%2Fwxauth%2Fcallback%3Fredirect%3DaHR0cHM6Ly9kdmx3Nmgud3gubnBvbGwubmV0L2FjdD9hY3Q9MjIzOTQ4&response_type=code&scope=snsapi_userinfo&state=&connect_redirect=1#wechat_redirect',headers=headers)
# cookies = requests.utils.dict_from_cookiejar(res.cookies)
# print(cookies)
# html=res.text
# #1、取所有物质url
# cookie=''
# soup = BeautifulSoup(html, 'lxml')
# for name,value in res.cookies.items():
#     cookie += '{0}={1};'.format(name, value)
# print(cookie)

app = Flask(__name__)
app.debug = True

# 具体导入配
# 根据需求导入仅供参考
app.config.fromobject(dict(WEIXIN_APP_ID='', WEIXIN_APP_SECRET=''))

#初始化
weixin = Weixin()
weixin.init_app(app)