"""
coding:utf-8
@Software:
@Time:2022/12/29 16:50
@Author:liaoqin
"""
import os
from faker import Faker

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
    print('success')

f = Faker(locale='zh_CN')

# a = '{"id":"144","policyName":"郭倩","policyDesc":"通过经验部分产品最后.分析历史这里建设位置建设.","securityPolicies":[{"messageId":"zy","messageName":"系统资源监控","policyStatus":true},{"messageId":"ap","messageName":"应用程序监控","policyStatus":false},{"messageId":"pr","messageName":"进程监控","policyStatus":false},{"messageId":"sv","messageName":"系统服务监控","policyStatus":false},{"messageId":"np","messageName":"网络端口监控","policyStatus":false}]}'
# a = '{"securityPolicies": [{"messageId": "zy","messageName": "系统资源监控","policyStatus": true}]}'
# a = eval(a)
# print(a, type(a))

if __name__ == '__main__':
    del_file('allureReports')