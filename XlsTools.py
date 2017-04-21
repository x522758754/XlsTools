#!user/bin/env python
# coding:utf-8

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# param
xlsDir = 'data'  # Xls 目录
outDir = 'output'  # txt 输出目录

# 获得目录下文件
# 类型为下xls或xlsx
# name 不包含 ~
def GetAllXls(path):
	#print path
	fileList = []
	for root, dirs, files in os.walk(path):
		for f in files:
			if(-1 == f.find('~') and (f.endswith('.xlsx') or f.endswith('.xls') )):
				fileList.append(f)
				

	return fileList

# 获得以_开头的sheet名
def GetSheets():
	pass