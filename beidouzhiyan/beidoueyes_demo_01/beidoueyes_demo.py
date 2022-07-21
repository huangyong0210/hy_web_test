# -*- coding = utf-8 -*-
# @Time : 2022/7/18 11:33
# @Author : huangyong
# @File : beidoueyes_demo.py
# @software : PyCharm

from beidou_driver import BeidouDriver
from selenium.webdriver.common.by import By


# TODO：后面这些验证程序要放到其他文档，按迭代，版本，来管理
from beidouzhiyan.beidou_v3 import notice_set_test
from collections import namedtuple
from beidouzhiyan.beidou_v3.notice_set_test import check_menu, check_function

if __name__ == '__main__':

    # 主程序在这里开始, 默认mode是debug，不截屏; -1代表最大化屏幕
    demo = BeidouDriver(window_size=(-1, -1))
    demo.login("0625", "123456")
    # 验证登录
    text = demo.is_valid_info(By.XPATH, r"/html/body/div[2]/p", False)
    if text != "":
        print(text)
        exit(1)  # 没有登录后面不用跑了。

    # TODO：每个测试用例用一个方法封装起来
    # TODO：验证数据以后可以通过其他文本录入如Excel，txt，或者数据库读取
    list_menu = ["赛事活动", "活动报名", "直播管理", "安全预警", "设备指令"]
    check_menu_res = check_menu(demo, list_menu)



    # TODO:每个menu若存在，进入其验证程序
    for i, section in enumerate(list_menu):
        if check_menu_res[i]:
            print(f"调用{section}对应测试用例")
            # 模拟调用其中得安全预警模块
            if i == 3:
                # 点击进入页面
                demo.driver.find_element(By.XPATH, r"/html/body/div/div/div[2]/div/div[4]").click()
                # 进行页面验证
                notice_set_test.check_page_text(demo, notice_set_test.expect_text_list)
                print(f"{section}测试完成")

                # 模拟调用其中得设备指令模块
            if i ==4 :
                        # 点击进入页面
                demo.driver.find_element(By.XPATH, r"/html/body/div/div/div[2]/div/div[5]").click()
                        # 进行页面验证
                notice_set_test.check_page_text_02(demo, notice_set_test.expect_text_list_01)
                print("开始测试功能")
                list_function = ["重启","恢复出厂","远程关机","禁止关机","上传频度","设置IP或域名","设置端口","允许关机","关闭休眠"]
                check_function_res = check_function(demo,list_function)
                print(f"{section}测试完成")
        else:
            print(f"{section}不存在")








    # demo.driver.close()  # 最后关闭浏览器
    # TODO: 把每一个测试做成任务调度
    # TODO：做web网站交互，启动任务调度，查看运行情况，修改测试用例等

