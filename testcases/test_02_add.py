"""
coding:utf-8
@Software:
@Time:2022/12/19 16:58
@Author:liaoqin
"""
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_mysql import db
from common.handle_log import my_log
from common.tools import random_name
from common.handle_mysql import my_key
import os, pytest, requests

class TestAdd:
    r_name = random_name()
    excel = HandleExcel(os.path.join(DATA_DIR, 'QCD.xlsx'), 'add')
    datas = excel.read_excel_data()
    base_url = conf.get('server_info', 'server_url')

    @pytest.mark.parametrize('item', datas)
    def test_add(self, item, qjmj_login_cls):

        url = self.base_url + item['url']
        headers = getattr(qjmj_login_cls, 'headers')

        item['data'] = item['data'].replace('#name#', self.r_name)
        payload = eval(item['data'])
        method = item['method']
        requests.request(url=url, headers=headers, json=payload, method=method)
        item['excepted'] = item['excepted'].replace('#name#', self.r_name)
        excepted = eval(item['excepted'])

        try:
            if item['check_sql']:
                a_name = db.find_one(item['check_sql'])
                assert my_key(a_name) == excepted['name']
            my_log.info("用例：{} ----用例成功".format(item['title']))
        except Exception as e:

            my_log.error("用例：{} ----用例失败".format(item['title']))
            my_log.exception(e)

            raise e













