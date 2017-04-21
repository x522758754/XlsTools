#!/user/bin/env python
# coding:utf-8


import sys
import os
import xlrd

from XlsTools import *

# sys init之后
reload(sys)
# coding:utf-8 定义源代码的编码，如果没定义，此远吗中是不可以包含中文字符的
# 设置默认的string的编码格式
sys.setdefaultencoding('utf-8')


if('__main__' == __name__):
    print(u'---------------程序开始-----------')

    if(2 == len(sys.argv)):
        xlsDir = sys.argv[1]

    if(not os.path.exists(xlsDir)):
    	os.mkdir(xlsDir)

    if(3 == len(sys.argv)):
        outDir = sys.argv[2]

    if(not os.path.exists(outDir)):
        os.makedirs(outDir)

    print(u'数据目录: ' + xlsDir)
    print(u'输出目录: ' + outDir)

    fileList = GetAllXls(xlsDir)

    for f in fileList:
    	data = xlrd.open_workbook(xlsDir + os.path.sep + f)
    	sheets = data.sheets()
    	for sheet in sheets:
    		if(0 == sheet.name.find('_')):
    			fileName = f[0:f.find(.)] + sheet.name
    			HandleXlsToTxt(fileName, sheet)
