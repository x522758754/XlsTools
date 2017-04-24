#!/user/bin/env python
# coding:utf-8


import sys
import os
import xlrd

from XlsCommon import *

# sys init之后
reload(sys)
# coding:utf-8 定义源代码的编码，如果没定义，此远吗中是不可以包含中文字符的
# 设置默认的string的编码格式
sys.setdefaultencoding('utf-8')


_XlsDir = 'data'  # Xls 目录
_OutDir = 'output'  # txt 输出目录
_bError = False #是否出错

_KeyExplain = 0 # sheet第一行：每一个的字段注释说明
_TypeRow = 1 # sheet第二行：每一个的字段的类型
_ClientKeysRow = 2 # sheet第三行: 客户端字段名（备注：服务器表此行可以为空))
_ServerKeysRow = 3 # sheet第四行：服务器字段名（备注：客户端表此行可以为空))
_DataRow = 4 # sheet第五行：数据开始行
_EnumFalg = '*' #枚举相关的标志

_TxtSplit = '\t'


# 解析客户端表
# 将Xls的一个sheet =》 txt
# dictName：组装的数据表文件名
# sheet： Xls中一个Sheet数据结构
def ClientSheetToTxt(fileName, sheet):
	txtName = FormatTxtName(fileName + sheet.name)

	dictType = CheckSheet(sheet)
	if(-1 == dictType):
		print(u'表: %s 为无效表，请检查表头' % (txtName))
		_bError = True
		return

	print(u'******解析表:%s*******' % (txtName))

	colIds = GetClientKeyIndexs(sheet)
	typeIds = GetTypeIds(sheet)
	lastRowIndex = GetLastRowIndex(sheet)
	for colId in colIds:
		rowData = []
		type = sheet.cell_value(_TypeRow, colId)
		for rowId in range(_DataRow, lastRowIndex):
			value = sheet.cell_value(rowId, colId)
			ParseData(type, value)


# 规范数据表的文件名
def FormatTxtName(name):
	txtName = ''
	arrayString = name.lower().split('_')
	for i in range(len(arrayString)):
		if(len(arrayString[i])):
			if(0 == i):
				txtName = arrayString[i]
			else:
				txtName = txtName + '_' + arrayString[i]

	return txtName


#解析xls中的CellValue的值
def ParseData(originData, type):
	pass



# 程序执行开始
if('__main__' == __name__):
	print(u'---------------程序开始-----------')

	if(2 == len(sys.argv)):
		_XlsDir = sys.argv[1]

	if(not os.path.exists(_XlsDir)):
		os.mkdir(_XlsDir)

	if(3 == len(sys.argv)):
		_OutDir = sys.argv[2]

	if(not os.path.exists(_OutDir)):
		os.makedirs(_OutDir)

	print(u'数据目录: ' + _XlsDir)
	print(u'输出目录: ' + _OutDir)

	fileList = GetAllXls(_XlsDir)

	for f in fileList:
		data = xlrd.open_workbook(_XlsDir + os.path.sep + f)
		sheets = data.sheets()
		for sheet in sheets:
			if(0 == sheet.name.find('_')):
				fileName = f[0:f.find('.')]
				ClientSheetToTxt(fileName, sheet)

	print(u'---------------程序结束-----------')

	if(_bError):
		print(u'程序出错，请检查出错的地方')
