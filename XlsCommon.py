#!user/bin/env python
# coding:utf-8

import os
import sys
import xlrd
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

# 参数配置
_KeyExplain = 0 # sheet第一行：每一个的字段注释说明
_TypeRow = 1 # sheet第二行：每一个的字段的类型
_ClientKeysRow = 2 # sheet第三行: 客户端字段名（备注：服务器表此行可以为空))
_ServerKeysRow = 3 # sheet第四行：服务器字段名（备注：客户端表此行可以为空))
_DataRow = 4 # sheet第五行：数据开始行
_EnumFalg = '*' #枚举相关的标志

_TxtSplit = '\t'


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

# 检测此表的类型，无效表(-1)、客户端（0）、服务器（1）、还是都有（2）
def CheckSheet(sheet):
	if(3 > sheet.nrows or 2 > sheet.ncols):
		return -1

	dictType = -1
	clientKeyValues = sheet.row_values(_ClientKeysRow)
	if(0 != len(clientKeyValues) and 0 != len(clientKeyValues[0])):
		dictType = 0


	serverKeyValues = sheet.row_values(_ServerKeysRow)
	if(0 != len(serverKeyValues) and 0 != len(serverKeyValues[0])):
		if(0 == dictType):
			dictType = 2
		else:
			dictType = 1

	return dictType

# 获得sheet的类型有效列索引列表(不包含枚举)
# 中间不允许有空列
def GetTypeIds(sheet):
	typeIds = []

	types = sheet.row_values(_TypeRow)
	for i in range(len(types)):
		if(0 != len(types[i])):
			if(types[i].startswith('*')):
				continue
			typeIds.append(i)
		else:
			#有空列，则后续则视为无效列
			break

	return typeIds

# 客户端有效列索引列表(不包含枚举)
def GetClientKeyIndexs(sheet):
	clientIds = []

	typeIds = GetTypeIds(sheet)
	keys = sheet.row_values(_ClientKeysRow)
	for i in range(len(keys)):
		if(0 != len(keys[i])):
			#先判断此索引是否有对应的类型
			for typeId in typeIds:
				if(i == typeId):
					clientIds.append(i)
					break
		else:
			if(i == 0):
				break
			else:
				continue


	return clientIds

#服务器有效列索引列表(不包含枚举)
def GetServerKeyIndexs(sheet):
	serverIds = []

	typeIds = GetTypeIds(sheet)
	keys = sheet.row_values(_ServerKeysRow)
	for i in range(len(keys)):
		if(0 != len(keys[i])):
			#先判断此索引是否有对应的类型
			for typeId in typeIds:
				if(i == typeId):
					serverIds.append(i)
					break
		else:
			if(i == 0): #索引不许为空
				break

	return serverIds

#客户端枚举索引列表
def GetClientEnumIndexs(sheet):
	enumIds = []

	keys = sheet.row_values(_ClientKeysRow)
	for i in range(len(keys)):
		if(keys[i].startswith('*')):
			enumIds.append(i)

	return enumIds

#数据的最后一行索引,不允许中间行有未填写的数据
def GetLastRowIndex(sheet):
	lastRowIndex = -1
	for i in range(4, sheet.nrows):
		row_values = sheet.row_values(i)
		for value in row_values:
			if(0 == len(str(value))):
				break
		lastRowIndex = i

	return lastRowIndex

#打开文件
def OpenFile(fileName, mode = 'w', code = 'utf-8'):
	f = codecs.open(fileName, mode, code)
	return f
#写数据到一个已打开文件中
def WriteLineData(fileOpen, data):
	strLine = ''
	for i in range(len(data)):
		strLine += str(data[i])
		if(i < len(data) - 1):
			strLine += _TxtSplit

	fileOpen.write(strLine + '\n')