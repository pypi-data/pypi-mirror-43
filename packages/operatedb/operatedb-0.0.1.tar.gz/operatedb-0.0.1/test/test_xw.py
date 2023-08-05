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
import re

pattern = '增持|减持|股权变动|权益变动|股东.*买入|实控人.*变更|实际控制人.*变更|质押|冻结|爆仓|战略投资|注资|抽逃资金|股东.*退出|引入.*投资|实际控制人|被动减持|解质|解押|解冻|股东|实际控制人|实控'
#
# # print(str.split('|'))
# str.encode('utf8')
# d = re.match('增持', '徐威增持')

# p=re.compile('增持')
# r=p.search('徐威增持')
# print(r)
#
# print(d)

#检测是否匹配
def parse(txt,pattern):
    if type(txt).__name__!='str':
        return False
    p=re.compile(pattern)
    r=p.search(txt)
    if r and r.group():
        print(1)
        return True
    else:
        print(2)
        return False
#

a = ['x','w']
b = ['x']
print(a - b)