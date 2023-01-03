'''
coding:utf-8
@Software:登录
@Time:2022/12/12 14:11
@Author:xiaoshiwen
'''
from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_log import my_log
from common.handle_mysql import db
import os, requests, pytest
from common.handle_path import DATA_DIR



class TestSelect:
    #第一步：从excel读数据
    excel = HandleExcel(os.path.join(DATA_DIR, 'QCD.xlsx'), 'select')
    datas = excel.read_excel_data()
    base_url = conf.get("server_info","server_url")

    @pytest.mark.parametrize('item', datas)
    def test_select(self, item, qjmj_login_cls):#4、qjmj_login调用类登录前置方法
        """
        登录
        :return:
        """
        #第二步：准备测试用例数据
        url = self.base_url + item['url']
        payload = item['data']
        method = item['method']

        #5、通过用例前置调用类属性值
        headers = getattr(qjmj_login_cls, 'headers')

        #第三步：发送请求
        response = requests.request(method=method,url=url,json=payload,headers=headers)
        res = response.json()


        #第四步：断言
        try:
            if item['check_sql']:
                count = db.find_count(item['check_sql'])
                assert res['totalElements'] == count
            my_log.info("用例：{} ----用例成功".format(item['title']))
        # 第五步：写日志
        except Exception as e:
            my_log.error("用例：{} ----用例失败".format(item['title']))
            my_log.exception(e)
            raise e








