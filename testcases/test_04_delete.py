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
from common.handle_mysql import db
from common.handle_log import my_log
from faker import Faker


class TestDelete:
    f = Faker(locale='zh_CN')
    r_name = f.name()
    sql_id = str(db.find_one('SELECT id from monitor_security_group WHERE id != 1 ORDER BY RAND() LIMIT 1')['id'])
    excel = HandleExcel(os.path.join(DATA_DIR, 'QCD.xlsx'), 'delete_safe')
    datas = excel.read_excel_data()
    base_url = conf.get('server_info', 'server_url')

    @pytest.mark.parametrize('item', datas)
    def test_add_safe(self, item, qjmj_login_cls):

        url = self.base_url + item['url']
        headers = getattr(qjmj_login_cls, 'headers')

        item['data'] = item['data'].replace('#id#', self.sql_id)
        payload = eval(item['data'])
        method = item['method']
        requests.request(url=url, headers=headers, json=payload, method=method)
        # res = response.json()
        # item['excepted'] = item['excepted'].replace('#paramDC#', self.r_name)
        excepted = eval(item['excepted'])

        try:
            # assert res['policyName'] == excepted['policyName']
            if item['check_sql']:
                item['check_sql'] = item['check_sql'].replace('#id#', self.sql_id)
                p_name = db.find_one(item['check_sql'])
                assert p_name == excepted['policy_name']
            my_log.info("用例：{} ----用例成功".format(item['title']))
        except Exception as e:

            my_log.error(f"用例：{item['title']} ----用例失败")
            my_log.exception(e)

            raise e


