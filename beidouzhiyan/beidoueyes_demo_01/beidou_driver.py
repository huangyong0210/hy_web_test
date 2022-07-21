# -*- coding = utf-8 -*-
# @Time : 2022/7/18 10:48
# @Author : huangyong
# @File : beidou_driver.py
# @software : PyCharm
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec

from settings import BASE_URL, CHROME_EXE, CHROME_DRIVER, IMPLICITLY_WAIT, BUG_PROJECT_ID, DEBUG, LOG_ROOT, \
    SCREENSHOT_ROOT, BASE_DIR, BUG_IDENTIFIER, ACCESS_TOKEN
from tools import log_init, create_bug, get_project_id, get_pingcode_token, upload_file_pingcode


class BeidouDriver(object):
    """
    构建一个北斗之眼测试对象，包含浏览器初始化，日志初始化，验证流程（截屏和提交bug）
    """
    def __init__(
            self,
            log_file_name: str = None,
            window_size: tuple = (1920, 1080),
            chrome_exe: str = None,
            chrome_driver: str = None):

        # 检测是否有log文件夹和截屏文件夹
        log_path = os.path.join(BASE_DIR, LOG_ROOT)
        self.screenshot_path = os.path.join(BASE_DIR, SCREENSHOT_ROOT)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)

        if log_file_name is None:
            today = datetime.today()
            time_str = today.strftime('%Y%m%d_%H%M%S')
            log_file_name = os.path.join(log_path, f"{time_str}.log")

        self.log = log_init(log_file_name)
        self.is_debug = DEBUG
        self.bug_access_token = ACCESS_TOKEN
        self.bug_project_id = self.init_pingcode()

        self.log.info("初始化浏览器")
        self.driver = self.init_driver(chrome_exe, chrome_driver)
        if window_size[0] == -1 or window_size[1] == -1:
            # -1 代表最大化屏幕
            self.driver.maximize_window()
        else:
            self.driver.set_window_size(window_size[0], window_size[1])
        self.log.info("初始化成功")

    @staticmethod
    def init_driver(chrome_exe: str, chrome_driver: str) -> webdriver:
        """
        初始化浏览器
        :param chrome_exe:
        :param chrome_driver:
        :return: 浏览器实例
        """
        option = webdriver.ChromeOptions()
        if chrome_exe:
            option.binary_location = chrome_exe
        else:
            option.binary_location = CHROME_EXE
        if chrome_driver:
            s = Service(chrome_driver)
        else:
            s = Service(CHROME_DRIVER)
        dr = webdriver.Chrome(service=s)
        dr.implicitly_wait(IMPLICITLY_WAIT)
        return dr

    def init_pingcode(self) -> str:
        """
        初始化pingcode配置
        :return: 返回项目ID
        """
        self.log.info("初始化pingcode配置")
        bug_project_id = get_project_id(BUG_IDENTIFIER, ACCESS_TOKEN)
        if bug_project_id:
            if bug_project_id != BUG_PROJECT_ID:
                self.log.warning(f"项目ID({bug_project_id})与配置设置的项目ID({BUG_PROJECT_ID})不一样，请检测配置")
        else:
            self.log.warning("初始化pingcode配置不成功")
            self.log.info("尝试更新token")
            access_token = get_pingcode_token()
            if access_token:
                self.log.info(f"更新token成功，新token={access_token}")
                print(f"更新token成功，新token={access_token}")
                self.bug_access_token = access_token
                bug_project_id = get_project_id(BUG_IDENTIFIER, access_token)
                if bug_project_id:
                    if bug_project_id != BUG_PROJECT_ID:
                        self.log.warning(f"项目ID({bug_project_id})与配置设置的项目ID({BUG_PROJECT_ID})不一样，请检测配置")
            else:
                self.log.warning("更新token不成功")
                print(f"更新token不成功，若需要编写缺陷，请及时更新token")
                self.bug_access_token = ""

        return bug_project_id

    def login(self, username: str, passwd: str) -> None:
        """
        登录平台
        :param username:
        :param passwd:
        :return:
        """
        self.log.info(f"登录平台, 账号：{username}")
        self.driver.get(f"{BASE_URL}/login")
        # 填入账号密码
        self.driver.find_element(
            By.XPATH,
            r"/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div/div/input").send_keys(username)

        self.driver.find_element(
            By.XPATH,
            r"/html/body/div[1]/div/div[2]/div[2]/form/div[2]/div/div/input").send_keys(passwd)

        self.driver.find_element(
            By.XPATH,
            r"/html/body/div[1]/div/div[2]/div[2]/form/div[3]/div/button").click()

    # TODO: 后期可以还有其他验证方式，如连接是否存在，提示信息是否正确等，可以用不同方法实现   #专门用作验证的方法
    def is_valid_text(self, by_type: By, check_element: str, value: str, dr: webdriver = None) -> bool:
        """
        验证元素是否和设定的一致
        :param dr: 如果dr没有数据，换全局driver
        :param by_type: 定位方式
        :param check_element: 定位数据
        :param value: 期望值
        :return:
        """
        self.log.info(f"验证信息：{value}")
        is_success = False
        res_text = ""

        try:
            if check_element != "":
                if dr is None:
                    dr = self.driver
                element = dr.find_element(
                    by_type,
                    check_element)
            else:
                # 如果check_element为空字符串，直接获取dr的text
                if dr is None:
                    self.log.error(f"没有定位元素check_element, 则dr必须是改元素对象")
                    return is_success
                element = dr
            res_text = element.get_attribute("innerText").strip()
            if res_text == value:
                self.log.info(f"验证信息{value}-成功")
                is_success = True
        except Exception as e:
            self.log.info(f"验证信息{value}-失败")
            self.log.error(e)

        if not is_success:
            # 错误截屏
            file_name = self.screenshot(value)
            text = f"验证失败, 期望信息：{value},获取信息：{res_text}"
            self.log.info(f"{text},截屏文档：{file_name}")
            self.create_bug(text, text, file_path=file_name)

        return is_success

    def is_valid_info(self, by_type: By, check_element: str, expect_res: bool, dr: webdriver = None) -> str:
        """
        验证元素是否和设定的一致
        :param dr: 如果dr没有数据，换全局driver
        :param by_type: 定位方式
        :param check_element: 定位数据，如果为“”，直接验证dr的文本
        :param value: 期望值
        :return:
        """
        self.log.info(f"验证是否有提示信息")
        if dr is None:
            dr = self.driver
        res_text = ""
        has_element = True
        try:
            element = dr.find_element(
                by_type,
                check_element)
            res_text = element.get_attribute("innerText")
        except Exception as e:
            has_element = False
            self.log.info(f"没有提示信息")
            if expect_res:
                self.log.error(e)

        if not expect_res == has_element:
            # 错误截屏
            file_name = self.screenshot("valid_info")
            self.log.info(f"验证失败, 截屏文档：{file_name}")
            text = f"验证失败, 期望元素是否存在：{expect_res}，元素文本值：{res_text}"
            self.create_bug(text, text, file_path=file_name)

        return res_text


    def screenshot(self, prefix: str = "screen") -> str:
        today = datetime.today()
        time_str = today.strftime('%Y%m%d_%H%M%S')
        file_name = f"{prefix}_{time_str}_bug.png"
        self.driver.save_screenshot(os.path.join(self.screenshot_path, file_name))
        return file_name

    def create_bug(self, title: str, description: str, file_path: str = "") -> str:
        """
        在pingcode对应项目中创建缺陷
        :param title: 缺陷题目
        :param description: 缺陷描述
        :param file_path: 缺陷附件
        :return:
        """
        if self.is_debug:
            self.log.info("debug模式不提交缺陷")
            return ""
        bug = create_bug(title, description, BUG_IDENTIFIER, self.bug_access_token, project_id=self.bug_project_id)
        if bug:
            self.log.info(f"成功创建缺陷：{bug['identifier']}")
            if file_path:
                res = upload_file_pingcode(bug['id'], file_path, self.bug_access_token)
                if res:
                    self.log.info(f"上传截图{file_path}成功")
                else:
                    self.log.warning(f"上传截图{file_path}不成功")
            return bug["id"]
        else:
            return ""

    def implicitly_wait(self, param):
        pass


if __name__ == '__main__':
    demo = BeidouDriver(window_size=(-1, -1))

