# -*- coding = utf-8 -*-
# @Time : 2022/7/18 10:47
# @Author : huangyong
# @File : settings.py
# @software : PyCharm
import os
# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True  # 是否为生产环境，测试环境不进行缺陷提交

# 文档路径设置
LOG_ROOT = "logs"
SCREENSHOT_ROOT = "screenshot"

# 测试网站设置
BASE_URL = "https://test-m.beidoueyes.cn"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_DRIVER = r"E:\软件测试\chromedriver.exe"
IMPLICITLY_WAIT = 5  # 隐式等待

# PingCode配置
PING_CODE_BASE_URL = 'https://open.pingcode.com'  # 接口地址
# PING_CODE_AUTO_URL = "https://rest_api_root"
PING_CODE_CID = 'IpXyRzDumVQd'
PING_CODE_SECRET = 'bPPKaRQQmDIqGiMVAvjJRAqh'
BUG_PROJECT_ID = '604f5840941768a1115f43ba'  # 项目ID
BUG_IDENTIFIER = 'ZDQ'  # 这个是项目缩写
ACCESS_TOKEN = "8d079bfb-9f68-4eea-a183-8a5fc2a13b40"  # 30天有效
