# -*- coding: utf-8 -*-
"""
-----------------------------
 File Name：  run_tests
 Description :
 Author :  liuye
 date：   2017/9/3
 ----------------------------
"""
import sys, time
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data


test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')


if __name__ == '__main__':
    test_data.init_data()

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/'+ now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='Guest Manage Interface Test Report', description='Example')
    runner.run(discover)
    fp.close()