#!/user/bin/env python
# coding:utf-8

import sys
import os
import codecs
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

#删除的列 从0开始
DELCOL = 1
_DictFileCoding = dict()

def GetAllTxt(srcPath, dstPath):
	#print path
	srcfiles = []
	dstfiles = []
	for root, dirs, files in os.walk(srcPath):
		for f in files:
			if f.endswith('.txt'):
				srcfile = os.path.join(root, f)
				srcfiles.append(srcfile)
				#filePath = filePath.replace('\\','/')
				dstfile = srcfile.replace(srcPath, dstPath, 1)
				dstfiles.append(dstfile)
	return srcfiles, dstfiles

def handleEncoding2Utf(original_file,newfile):
	#newfile=original_file[0:original_file.rfind(.)]+'_copy.csv'
	f=open(original_file,'rb+')
	content=f.read()#读取文件内容，content为bytes类型，而非string类型
	source_encoding='utf-8'
	#####确定encoding类型
	try:
		content.decode('utf-8').encode('utf-8')
		source_encoding='utf-8'
	except:
		try:
			content.decode('gbk').encode('utf-8')
			source_encoding='gbk'
		except:
			try:
				content.decode('gb2312').encode('utf-8')
				source_encoding='gb2312'
			except:
				try:
					content.decode('gb18030').encode('utf-8')
					source_encoding='gb18030'
				except:
					try:
						content.decode('big5').encode('utf-8')
						source_encoding='gb18030'
					except:
						content.decode('cp936').encode('utf-8')
						source_encoding='cp936'
	f.close()
	
	#####按照确定的encoding读取文件内容，并另存为utf-8编码：
	block_size=4096
	#print(original_file, source_encoding)
	dstDir = os.path.dirname(newfile)
	if not os.path.exists(dstDir):
		os.makedirs(dstDir)
	with codecs.open(original_file,'r',source_encoding) as f:
		with codecs.open(newfile,'w','utf-8') as f2:
			while True:
				content=f.read(block_size)
				if not content:
					break
				f2.write(content)
				_DictFileCoding[newfile] = source_encoding


def handleEncodingUtf2(original_file, newfile, coding = 'gbk'):
	block_size=4096
	source_encoding = 'utf-8'
	#print(original_file, source_encoding)
	dstDir = os.path.dirname(newfile)
	if not os.path.exists(dstDir):
		os.makedirs(dstDir)
	with codecs.open(original_file,'r',source_encoding) as f:
		with codecs.open(newfile,'w', coding) as f2:
			while True:
				content=f.read(block_size)
				if not content:
					break
				f2.write(content)

def DelRowFile(srcPath, dstPath):
	dir = os.path.dirname(dstPath)
	if not os.path.exists(dir):
		os.makedirs(dir)
	with open(srcPath) as fp_in:
		with open(dstPath, 'w') as fp_out:
			#fp_out.writelines(line for i, line in enumerate(fp_in) if i != DELROW)
			for line in fp_in.readlines():
				print line
				fp_out.write(line)

def DelColFile(srcPath):
	#df = pd.read_csv(srcPath, encoding='utf-8')
	df = pd.read_csv(srcPath,sep='\t',header=None, encoding='utf-8',)
	df.drop([df.columns[DELCOL]], axis=1, inplace=True)
	df.to_csv(srcPath, sep='\t',header=None, encoding='utf-8',index=None)


def main(argv):
	#temp='TaskConfig'
	#handleEncoding2Utf('Data/public/' + temp +'.txt', 'Dat/' + temp +'.txt')
	#DelColFile('Dat/' + temp +'.txt')
	#handleEncodingUtf2('Dat/' + temp +'.txt', 'Da/' + temp +'.txt')
	#return
	src = ""
	dst = ""
	if(len(argv) != 3):
		#return
		src = 'Data'
		dst = 'Datas'
	else:
		src = argv[1]
		dst = argv[2]
	if not os.path.exists(src):
		print u'Error! ----------------原始目录：%s 不存在' %(src)
		return
	print u'----------------原始目录 %s---------------' %(src)
	print u'----------------目标目录 %s---------------' %(dst)
	srcfiles, dstfiles = GetAllTxt(src, dst)
	fLen = len(srcfiles)
	for i in range(fLen):
		src_file = srcfiles[i]
		dst_file = dstfiles[i]
		handleEncoding2Utf(src_file, dst_file)
		DelColFile(dst_file)
		handleEncodingUtf2(dst_file, src_file,_DictFileCoding[dst_file])

if('__main__' == __name__):
	main(sys.argv)


