# -*- coding = utf-8 -*-
# @Time : 2022/7/18 10:47
# @Author : huangyong
# @File : tools.py
# @software : PyCharm
import logging
import requests
from typing import Dict

from beidouzhiyan.beidoueyes_demo_01.settings import PING_CODE_BASE_URL, PING_CODE_CID, PING_CODE_SECRET


def log_init(file_name: str, mode: str = 'w') -> logging:
    level = logging.INFO
    file_handler = logging.FileHandler(file_name, mode=mode, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s_[line:%(lineno)d]_%(levelname)s_%(message)s'))
    my_log = logging.Logger("beidou", level=level)
    my_log.addHandler(file_handler)
    return my_log


def get_project_id(identifier: str, token: str) -> str:
    """
    通过项目名称，获取项目ID
    :param identifier: 项目名称
    :param token:
    :return: ID
    """
    url = f'{PING_CODE_BASE_URL}/v1/agile/projects'
    data = {
        'access_token': token,
        'identifier': identifier
    }
    res = requests.get(url, params=data, headers={"Connection": "close"})
    res = res.json()
    if res.get("code") == "100026":
        print(res.get("message"), "获取项目ID失败,请刷新token")
        return ""
    if len(res["values"]) > 0:
        return res["values"][0]['id']  # 获取项目ID
    return ""


def get_pingcode_token() -> str:
    url = f'{PING_CODE_BASE_URL}/v1/auth/token?grant_type=client_credentials&client_id={PING_CODE_CID}&client_secret={PING_CODE_SECRET}'
    res = requests.get(url, headers={"Connection": "close"})
    res = res.json()
    return res['access_token']


def create_bug(title: str, description: str, identifier: str, token: str, project_id: str = None) -> Dict:
    try:
        if project_id is None:
            project_id = get_project_id(identifier, token)
            print(f"project_id={project_id}")

        if project_id == "":
            print("没有找到project_id")
            return {}

        url = f'{PING_CODE_BASE_URL}/v1/agile/bugs'
        data = {
            'access_token': token,
            "project_id": project_id,
            "title": title,
            "description": description,
        }
        res = requests.post(url, data=data)
        res = res.json()
        if res.get("code") == "100026":
            print(res.get("message"), "创建缺陷失败, 请刷新token")
            return {}
        if res.get("id"):
            return {
                "id": res.get("id"),
                "identifier": res.get("identifier")
            }
    except Exception as e:
        print("create bug error")
        print(e)

    return {}


def upload_file_pingcode(bug_id: str, file_path: str, token: str) -> bool:
    """
    在上面中上传附件
    :param bug_id: 缺陷对应ID
    :param token: 授权令牌
    :param project_id: 项目ID
    :param file_path: 文档路径
    :return: 返回True代表上传成功
    """
    url = f'{PING_CODE_BASE_URL}/v1/project/work_items/{bug_id}/files?access_token={token}'
    files = {
        "pic": (file_path, open(file_path, "rb"), "images/png")
    }
    try:
        res = requests.post(url=url, files=files)
        res = res.json()
        if res.get("code") == "100026":
            print(res.get("message"), "上传附件失败, 请刷新token")
            return False
        if res.get("id"):
            return True
    except Exception as e:
        print(e)

    return False


if __name__ == '__main__':
    # 测试通，能自动提bug到pingcode上
    # get_pingcode_token()
    token1 = "3f00f422-9c8b-4882-bce1-41e50cb92868"
    bug = create_bug(
        "python test bug 1234", "<h1>这里是描述,支持html格式</h1>", "ZDQ", token1, project_id="604f5840941768a1115f43ba")
    print(bug)
    #r = upload_file_pingcode(bug['id'], "screenshot/联系信息_20220713_100502.png", token1)
    #print(r)
