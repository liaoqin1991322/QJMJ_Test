"""
coding:utf-8
@Software:pytest中用来专门定义类前置、后置，用例级别前置后置方法  【注：文件名必须叫做 conftest.py】
@Time:2022/9/7 18:42
@Author:liaoqin
"""
import pytest,requests

from jsonpath import jsonpath
from common.handle_conf import conf

class BaseFixture:

   def __init__(self,headers):#定义类属性
       self.headers = headers


# @pytest.fixture(scope="class")  # 定义夹具，根据类运行
# def user_login_cls():
#     """定义类级别的前置和后置"""
#     """普通用户登录"""
#     # 1、准备登录账号和密码
#     head = eval(conf.get("server_info", "headers"))
#     params = {
#         "mobile_phone": conf.get("test_login", "mobile_phone"),
#         "pwd": conf.get("test_login", "pwd")
#     }
#     url = conf.get("server_info", "server_url") + "/member/login"
#     # 2、发送请求
#     response = requests.request(method="post", url=url, headers=head, json=params)
#     res = response.json()
#     # 3、提取token和用户id
#     token = jsonpath(res, "$..token")[0]  # jsonpath取出来是list，所以取里面的元素
#
#     # ********更新字典方法一*************************************************
#     # head['Authorization'] = "Bear " + token
#     # *******更新字典方法二**************************************************
#     head.update({'Authorization': "Bearer " + token})
#
#     # 4、设置为类属性，方法一
#     setattr(BaseFixture, "headers", head)
#     member_id = jsonpath(res, "$..id")[0]
#     setattr(BaseFixture, "member_id", member_id)
#
#     #yield  # 用yield隔开，用来区分前置和后置代码   【注：yield是一个关键字，它不是单独存在的，要写在fixture标记的固件中】
#     #yield 也可返回元组、列表、字典、字符串、对象等
#     yield BaseFixture #相当于yield前的是前置代码，返回一个BaseFixture对象
#
#     print("-----类级别的后置代码在编写")


# @pytest.fixture(scope="function")  #定义夹具，根据方法运行
# def case_login():
#     """定义用例级别的前置和后置"""
#     print("-----用例级别的前置代码在编写")
#
#     yield #用yield隔开，用来区分前置和后置代码   【注：yield是一个关键字，它不是单独存在的，要写在fixture标记的固件中】
#     print("-----用例级别的后置代码在编写")

@pytest.fixture(scope="class")
def qjmj_login_cls():#1、定义类用例前置
    """"""
    #登录成功，取返回
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI2MWY1YTE1NjkyYWU0YzJiYTc1MTI2ZTUyYTM3MTlmZiIsInVzZXIiOiJjYW96dW8iLCJyb2xlIjoi57O757uf5pON5L2c5ZGYIiwic3ViIjoiY2FvenVvIn0.Cpi0edw7G940l16Csp3T7TIfE5rCCK-1zrWWbMtK44fkXRr4qfkNwi5kj0Z_7DJi6Y04V02lfFBr0vzn4qfRfQ",
        'Content-Type': 'application/json'
    }

      # 2、设置类属性值
    # BaseFixture.headers = headers  #方法一：给类属性赋值
    setattr(BaseFixture, 'headers', headers)  # 方法二：给类属性赋值

    # a = BaseFixture.headers #方法一：类属性取值
    # getattr(BaseFixture,'headers') #方法二：类属性取值

    #3、返回类
    yield BaseFixture  # 相当于yield前的是前置代码，返回一个BaseFixture对象
    print("-----用例级别的后置代码在编写")
