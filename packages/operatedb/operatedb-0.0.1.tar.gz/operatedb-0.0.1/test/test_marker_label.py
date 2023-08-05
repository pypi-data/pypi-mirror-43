#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (C)2018 SenseDeal AI, Inc. All Rights Reserved
File: .py
Author: xuwei
Email: weix@sensedeal.ai
Last modified: date
Description:
'''

from marker_label import *
from multiprocessing import Pool




def cal_news_label():
    pattern = '增持|减持|股权变动|权益变动|股东.*买入|实控人.*变更|实际控制人.*变更|质押|冻结|爆仓|战略投资|注资|抽逃资金|股东.*退出|引入.*投资|实际控制人|被动减持|解质|解押|解冻|股东|实际控制人|实控'
    patternLabel = '权益变动'
    read_data = MarkerLabel('160','db_choice',pattern,patternLabel)


    news_id_list = pd.read_sql("""select a.INFOCODE as news_id from INFO_AN_NEWSBASIC a """,read_data.engine_db(),chunksize=1000)

    # p = Pool(processes=4)
    for id_list in news_id_list:
        id_tuple = tuple(id_list['news_id'].tolist())
        print('start')
        data_df = pd.read_sql("""select a.INFOCODE as news_id,a.TITLE as title,b.CONTENT as content from INFO_AN_NEWSBASIC a,INFO_AN_NEWSCONTENT b
                              where a.INFOCODE=b.INFOCODE and a.INFOCODE in {0}""".format(id_tuple),read_data.engine_db())

        write_result = MarkerLabel('160','db_test',pattern,patternLabel)
        write_result.cal_process(data_df, 'title', 'content', 'news_id', 'equity_changes_news_test1')
        # p.apply_async(write_result.cal_process, (data_df, 'title', 'content', 'news_id', 'equity_changes_news_test1',))
    # p.close()  # 关闭进程池，表示不能在往进程池中添加进程
    # p.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用


if __name__ == '__main__':
    cal_news_label()
    # cal_label = MarkerLabel('160', 'db_choice')
    # data = cal_label.cal_str_label('钢铁行业娱乐不死吃货的最高境界')

    # print(data)