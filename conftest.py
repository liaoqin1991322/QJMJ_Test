"""
coding:utf-8
@Software:用来专门定义类前置、后置，用例级别前置后置方法  【注：文件名必须叫做 conftest.py】
@Time:2022/9/7 18:42
@Author:liaoqin
"""
import pytest,requests

from jsonpath import jsonpath
from common.handle_conf import conf

class BaseFixture:

   def __init__(self,headers,member_id,loan_id,admin_member_id,admin_headers):
       self.headers = headers
       self.member_id = member_id
       self.loan_id = loan_id
       self.admin_member_id = admin_member_id
       self.admin_headers = admin_headers


@pytest.fixture(scope="class")  # 定义夹具，根据类运行
def user_login_cls():
    """定义类级别的前置和后置"""
    """普通用户登录"""
    # 1、准备登录账号和密码
    head = eval(conf.get("server_info", "headers"))
    params = {
        "mobile_phone": conf.get("test_login", "mobile_phone"),
        "pwd": conf.get("test_login", "pwd")
    }
    url = conf.get("server_info", "server_url") + "/member/login"
    # 2、发送请求
    response = requests.request(method="post", url=url, headers=head, json=params)
    res = response.json()
    # 3、提取token和用户id
    token = jsonpath(res, "$..token")[0]  # jsonpath取出来是list，所以取里面的元素

    # ********更新字典方法一*************************************************
    # head['Authorization'] = "Bear " + token
    # *******更新字典方法二**************************************************
    head.update({'Authorization': "Bearer " + token})

    # 4、设置为类属性，方法一
    setattr(BaseFixture, "headers", head)
    member_id = jsonpath(res, "$..id")[0]
    setattr(BaseFixture, "member_id", member_id)

    #yield  # 用yield隔开，用来区分前置和后置代码   【注：yield是一个关键字，它不是单独存在的，要写在fixture标记的固件中】
    #yield 也可返回元组、列表、字典、字符串、对象等
    yield BaseFixture #相当于yield前的是前置代码，返回一个BaseFixture对象

    print("-----类级别的后置代码在编写")


@pytest.fixture(scope="class")  # 定义夹具，根据类运行
def admin_login_cls():
    """定义类级别的前置和后置"""
    """管理员登录"""
    url = conf.get("server_info", "server_url") + "/member/login"
    admin_params = {
        "mobile_phone": conf.get("test_login", "admin_mobile"),
        "pwd": conf.get("test_login", "admin_pwd")
    }
    admin_headers = eval(conf.get("server_info", "headers"))
    admin_response = requests.request(method="post", url=url, json=admin_params, headers=admin_headers)
    admin_res = admin_response.json()

    admin_token = jsonpath(admin_res, "$..token")[0]
    admin_headers.update({'Authorization': "Bearer " + admin_token})
    # 4、设置为类属性，方法一
    setattr(BaseFixture, "admin_headers", admin_headers)
    member_id = jsonpath(admin_res, "$..id")[0]
    setattr(BaseFixture, "admin_member_id", member_id)

    # yield  # 用yield隔开，用来区分前置和后置代码   【注：yield是一个关键字，它不是单独存在的，要写在fixture标记的固件中】
    # yield 也可返回元组、列表、字典、字符串、对象等
    yield BaseFixture  # 相当于yield前的是前置代码，返回一个BaseFixture对象

    print("-----类级别的后置代码在编写")

@pytest.fixture(scope="function")  # 定义夹具，根据用例方法运行
def add_project():
    """定义用例级别的前置和后置"""
    """添加项目"""
    url = conf.get("server_info", "server_url") + "/loan/add"
    params = {
        "member_id": BaseFixture.member_id,
        "title": "测试数据--接口自动化",
        "amount": 200.00,
        "loan_rate": 12.0,
        "loan_term": 12,
        "loan_date_type": 1,
        "bidding_days": 5
    }
    response = requests.request(method="post", url=url, headers=BaseFixture.headers, json=params)
    res = response.json()
    BaseFixture.loan_id = jsonpath(res, "$..id")[0]
    yield BaseFixture  # 相当于yield前的是前置代码，返回一个BaseFixture对象

    print("-----类级别的后置代码在编写")



@pytest.fixture(scope="function")  # 定义夹具，根据用例方法运行
def audit_project():
    """定义用例级别的前置和后置"""
    """审核项目"""
    audit_url = conf.get("server_info", "server_url") + "/loan/audit"
    audit_params = {
         "loan_id": BaseFixture.loan_id,
        "approved_or_not": "true"
    }
    audit_response = requests.request(method="patch", url=audit_url, json=audit_params,
                                          headers=BaseFixture.admin_headers)  # 用管理员的请求头
    audit_res = audit_response.json()
    print("实际结果：", audit_res)
    yield audit_res  # 相当于yield前的是前置代码，返回一个BaseFixture对象

    print("-----类级别的后置代码在编写")


@pytest.fixture(scope="function")  #定义夹具，根据方法运行
def case_login():
    """定义用例级别的前置和后置"""
    print("-----用例级别的前置代码在编写")

    yield #用yield隔开，用来区分前置和后置代码   【注：yield是一个关键字，它不是单独存在的，要写在fixture标记的固件中】
    print("-----用例级别的后置代码在编写")