"""
coding:utf-8
@Software:所有用例执行的入口类
@Time:2022/8/16 18:02
@Author:liaoqin
"""

import pytest

# pytest.main()
pytest.main(['-vs', '-n=2',
            # 'testcases/test_01_select.py',
            # 'testcases/test_02_add.py',
            #  'testcases/test_03_update.py',
             'testcases/test_04_delete.py',
            #  'testcases/test_05add_audit.py',
            #  'testcases/test_06audit.py',
            # 'testcases/test_07invest.py',
            #  '--reruns','3', #重运行3次
            #  '--reruns-delay','3', #每3s运行一次
             '--alluredir=allureReports'
             ])
