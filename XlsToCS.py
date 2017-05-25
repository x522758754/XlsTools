#!user/bin/env python
# coding:utf-8

import sys
import os
from XlsCommon import *

reload(sys)
sys.setdefaultencoding('utf-8')

_XlsDir = 'data'  # Xls 目录
_OutDir = 'output'  #输出目录

_KeyExplain = 0 # sheet第一行：每一个的字段注释说明
_TypeRow = 1 # sheet第二行：每一个的字段的类型
_ClientKeysRow = 2 # sheet第三行: 客户端字段名（备注：服务器表此行可以为空))
_ServerKeysRow = 3 # sheet第四行：服务器字段名（备注：客户端表此行可以为空))
_DataRow = 4 # sheet第五行：数据开始行
_EnumFalg = '*' #枚举相关的标志

# 
def ClientSheetToCS(fileName, sheet):
	name = FormatName(fileName)

	dictType = CheckSheet(sheet)
	if(-1 == dictType):
		return
	elif(1 == dictType):
		return

	# 打开文件
	csName = name + 'DictLoader'
	dirPath = _OutDir + '/AutoDict/'
	fileOpen = OpenFile(dirPath+csName + '.cs')

	#DictModel 
	strModelClassName = name + 'DictModel' # 类名
	strModelItems = '' #成员字符

	#DictLoader
	strLoaderClassName = csName #类名
	strFileName = fileName # 文件名
	strLoaderItems = '' #解析函数成员字符
	
	colIds = GetClientKeyIndexs(sheet)
	for colId in colIds:
		keyExplain = sheet.cell_value(_KeyExplain, colId)
		type = sheet.cell_value(_TypeRow, colId)
		key = sheet.cell_value(_ClientKeysRow, colId)
		strModelItems += CreateModelItem(keyExplain, type, key)

		funcName = GetTypeSwitchFuncName(type)
		strLoaderItems += CreateLoaderItem(key, funcName, colId)

	strModel = CreateDictModel(strModelClassName, strModelItems)
	strLoader = CreateDictLoader(strLoaderClassName, strFileName,
		len(colIds), strModelClassName, strLoaderItems)

	strCSFile = CreateCSFile(GetSysData(), strModel, strLoader)

	fileOpen.write(strCSFile)
	fileOpen.close()

#
def ClientSheetToEnum(fileName, sheet):
	name = FormatName(fileName)
	dictType = CheckSheet(sheet)
	if(-1 == dictType):
		return
	elif(1 == dictType):
		return

	enumName = name + 'Enum'
	dirPath = _OutDir + '/AutoEnum/'
	fileOpen = OpenFile(dirPath+enumName + '.cs')

	#Enum
	strEnumName = enumName #目前只支持一个表一个枚举,所以采取文件名命名
	strEnumItems = ''

	lastRowIndex = GetLastRowIndex(sheet)
	colIds = GetClientEnumIndexs(sheet)
	for rowId in range(_DataRow, lastRowIndex):
		for colId in colIds:
			enumKey = str(sheet.cell_value(rowId, colId))
			enumDesc = str(sheet.cell_value(rowId, colId + 1))
			strEnumItems += CreateEnumItem(enumDesc, enumKey)

	strEnum = CreateEnumFile(GetSysData(), strEnumName, strEnumItems)
	fileOpen.write(strEnum)
	fileOpen.close()

# 格式化CS文件名
def FormatName(fileName):
	#name = fileName[0].upper() + fileName[1:] + 'DictLoader'
	name = ''
	arrayName = fileName.split('_')
	for i in range(len(arrayName)):
		if(len(arrayName[i]) > 0):
			str = arrayName[i][0].upper() + arrayName[i][1:]
			name += str
	return name

# 创建cs文件
def CreateCSFile(date, strModel, strLoader):
	strMain = '''
/**************************************************
* Author：Auto Generate
* Date: %s
* Desc:
* ************************************************/
namespace DataLoad
{
	[System.Serializable]
	%s

	%s
}

'''
	str = strMain %(date, strModel, strLoader)

	return str

# 创建class DictModel
def CreateDictModel(className, strItems):
	strMain = '''
	public class %s : DictModel
	{
		%s
	}
	'''
	str = strMain %(className, strItems)

	return str

# 创建DictModel成员
def CreateModelItem(keyExplain, type, key):
	strMain = '''
		/// <summary>
		/// %s
		/// </summary>
		public %s %s;
	'''
	str = strMain %(keyExplain, type, key)

	return str

# 创建class DictLoader
def CreateDictLoader(className, fileName, keyCount, modelClassName, strItems):
	strMain = '''
	public class %s : DictLoader
	{
		/// <summary>
		/// 获得表名
		/// </summary>
		protected override string GetFileName()
		{
			return "%s";
		}

		/// <summary>
		/// 解析行数据 => T
		/// </summary>
		/// <param name="rowData">每一行的数据</param>
		protected override DictModel ParseRowData(string[] rowData)
		{
			int keyCount = %s;
			%s model = new %s();
			%s

			return model;
		}
	}
	'''

	str = strMain %(className, fileName, keyCount,
		modelClassName, modelClassName, strItems)

	return str

# 创建DictLoader成员
def CreateLoaderItem(key, funcName, index):
	strMain = '''
			model.%s = DictTypeParse.%s(rowData[%s]);'''
	str = strMain %(key, funcName, index);

	return str

# 获取类型转换函数名
def GetTypeSwitchFuncName(type):
	funcName = ''
	if('int' == type):
		funcName = 'ToInt'
	elif('float' == type):
		funcName = 'ToFloat'
	elif('string' == type):
		funcName = 'ToString'
	elif('array_int' == type):
		funcName = 'ToArrayInt'
	elif('array_float' == type):
		funcName = 'ToArrayFloat'
	elif('array_string' == type):
		funcName = 'ToArrayString'
	else:
		print(u'错误的类型: %s' %(type))

	return funcName

# 创建枚举文件
def CreateEnumFile(date, enumName, enumItems):
	strMain = '''
/**************************************************
* Author：Auto Generate
* Date: %s
* Desc:
* ************************************************/
namespace DataLoad
{
	public enum %s : byte
	{
		%s
	}
}

'''
	str = strMain %(date, enumName, enumItems)

	return str

# 创建枚举项
def CreateEnumItem(enumDesc, enumKey):
	strMain = '''
		/// <summary>
		/// %s
		/// </summary>
		%s,
		'''
	str = strMain %(enumDesc, enumKey)

	return str


# 程序执行开始
if('__main__' == __name__):
	print(u'---------------XlsToCS程序开始-----------')

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
				ClientSheetToCS(fileName, sheet)
				ClientSheetToEnum(fileName, sheet)

	print(u'---------------XlsToCS程序结束-----------')
	os.system("pause")