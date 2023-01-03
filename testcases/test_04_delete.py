"""
coding:utf-8
@Software:
@Time:2022/12/29 17:15
@Author:liaoqin
"""
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
import os, pytest, requests
from common.handle_mysql import db, my_key
from common.handle_log import my_log


class TestDelete:
    excel = HandleExcel(os.path.join(DATA_DIR, 'QCD.xlsx'), 'delete')
    datas = excel.read_excel_data()
    base_url = conf.get('server_info', 'server_url')

    @pytest.mark.parametrize('item', datas)
    def test_delete(self, item, qjmj_login_cls):

        url = self.base_url + item['url']
        headers = getattr(qjmj_login_cls, 'headers')

        sql_id = str(my_key(db.find_one(item['sql_id'])))
        item['data'] = item['data'].replace('#id#', sql_id)
        payload = eval(item['data'])
        method = item['method']
        requests.request(url=url, headers=headers, json=payload, method=method)
        excepted = eval(item['excepted'])

        try:
            if item['check_sql']:
                item['check_sql'] = item['check_sql'].replace('#id#', sql_id)
                p_name = db.find_one(item['check_sql'])
                assert p_name == excepted['name']
            my_log.info("用例：{} ----用例成功".format(item['title']))
        except Exception as e:
            my_log.error("用例：{} ----用例失败".format(item['title']))
            my_log.exception(e)
            raise e



