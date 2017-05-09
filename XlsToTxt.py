#!/user/bin/env python
# coding:utf-8


import sys
import os
import xlrd
import codecs
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
_ArraySplit = '&&'


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

	print(u'****** 解析表: %s *******' % (txtName))

	#写文件
	fileOpen = OpenFile(_OutDir+'/'+fileName+'.txt')

	colIds = GetClientKeyIndexs(sheet)
	typeIds = GetTypeIds(sheet)
	lastRowIndex = GetLastRowIndex(sheet)
	for rowId in range(_DataRow, lastRowIndex):
		rowData = []
		for colId in colIds:
			type = sheet.cell_value(_TypeRow, colId)
			value = str(sheet.cell_value(rowId, colId))#转换成string
			rowData.append(ParseData(type, value))
		WriteLineData(fileOpen, rowData)

	fileOpen.close()

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
def ParseData(type, value):
	if(0 == cmp('int', type)):
		return ParseInt(type, value)
	elif(0 == cmp('float', type)):
		return ParseFloat(type, value)
	elif(0 == cmp('string', type)):
		return ParseString(type, value)
	elif(0 == cmp('array_int', type)):
		#遍历检查一下数组的值是否有问题
		arrayValue = value.split(_ArraySplit)
		for i in range(len(arrayValue)):
			strValue = arrayValue[i]
			ParseInt('int', strValue)

		return value
	elif(0 == cmp('array_float', type)):
		arrayValue = value.split(_ArraySplit)
		for i in range(len(arrayValue)):
			strValue = arrayValue[i]
			ParseInt('float', strValue)
	elif(0 == cmp('array_string', type)):
		return value
	else:
		_bError = True
		print(u'类型错误:未知类型%s' %(type))

#解析int数据
def ParseInt(type, value):
	if(0 == len(value)):
		return 0
	else:
		strValue = value
		if(-1 != value.find('.')):
			strValue = value[0:value.find('.')]
		try:
			iValue = int(strValue)
		except Exception as e:
			_bError = True
			print(u'类型转换:%s -> %s 出错' %(value, type))
			iValue = 0;
		finally:
			return iValue

#解析float数据
def ParseFloat(type, value):
	if(0 == len(value)):
		return 0.0
	else:
		strValue = value
		if(-1 != value.find('.')):
			strValue = value[0:value.find('.')]
		try:
			fValue = float(strValue)
		except Exception as e:
			_bError = True
			print(u'类型转换:%s -> %s 出错' %(value, type))
			fValue = 0.0
		finally:
			return fValue

#解析string数据
def ParseString(type, value):
	if(0 == len(value)):
		return ''
	else:
		return value



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
