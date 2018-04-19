#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 加载excel的名单

import xlrd
import xlwt
from datetime import date,datetime
from Test1 import Weibo
import time


def read_excel():

    # 设置编码
    xlrd.Book.encoding = "utf8"
    # 打开文件
    workbook = xlrd.open_workbook(u'矩阵微博登记信息.xlsx')
    table = workbook.sheet_by_index(0)
    rows_count = int(table.nrows)
    accounts = []
    for i in range(2,rows_count):

        nickname = table.row_values(i)[1].encode('utf-8')
        phone_num = str(int(table.row_values(i)[2]))
        username = str(int(table.row_values(i)[3]))
        password = table.row_values(i)[4].encode('utf-8')
        tags = (table.row_values(i)[5]).encode('utf-8').split("、")

        if username != '' and password != '':
            account = {}
            account['nickname'] = nickname
            account['phone_num'] = phone_num
            account['nickname'] = nickname
            account['password'] = password
            account['tags'] = tags
            wb = Weibo(username=username, password=password)
            wb.add_new("测试一下啊啊啊啊")
            if wb.login_success is True:
                account[tags[0]] = wb
                accounts.append(account)

            time.sleep(60)


if __name__ == '__main__':
    read_excel()