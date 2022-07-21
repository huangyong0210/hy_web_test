# -*- coding = utf-8 -*-
# @Time : 2022/7/20 10:55
# @Author : huangyong
# @File : test——011.py
# @software : PyCharm
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By


class TestCase:

    def test_001(self,username="0625",password=123456)
#初始化浏览器，进入网站
        driver = webdriver.Chrome()
        driver.get("https://test-m.beidoueyes.cn/login")

        #登录，输入账号，密码
        driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[2]/form/div[1]/div/div/input").send_keys(username)
        driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[2]/form/div[2]/div/div/input").send_keys(password)
        driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[2]/form/div[3]/div/button").click()








