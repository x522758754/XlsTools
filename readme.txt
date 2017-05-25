使用环境：

1.安装python:https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi
2.配置Python Path:
3.安装pip: python get-pip.py
4.使用pip 安装 xlrd（pip install xlrd）
或
1 python转exe，可py2exe或者pyinstaller，详细可网络搜索。

xls配表规范：

1. xls文件名小写，不同单词以'_'分隔,不允许存在同名的xls文件
2. xls的表名包含'_'为有效表名，否则则不进行解析
3. 第一行:字段说明 第二行:字段类型  第三行: 客户端字段名 第4行:服务器字段名 第5行：数据开始
4. '*':枚举相关标识,规则：*enum在前，*enumDesc 列数+1,且一个表一个枚举
5. '&&':数组分隔符
6. 如果某一列客户端需要而服务器不需要，则只需要在第三行填上对应的的字段名，第4行空着
7. 目前支持的类型 int、float、string、array_int、array_float、array_string、enum
8. 解析后，请检查是否有‘出错’字样，请检查出错的地方
