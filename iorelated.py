# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os


def detect_walk_search(root, nameList):
	''' 根据给出的根目录，寻找给出的文件名列表里的文件路径，和不同文件夹里的同名文件 '''
	fileCnt = 0
	folderCnt = 0
	existList = [0 for x in nameList]
	pathList = ["" for x in nameList]
	conflictList = []  # 一个文件在多个文件夹出现的情况
	for root, dirs, files in os.walk(root):
		for filename in files:
			fileCnt += 1
			fullpath = os.path.join(root,filename)
			for idx,name in enumerate(nameList):
				if name+".h" == filename:
					if not existList[idx]:
						existList[idx] = 1
						pathList[idx] = fullpath.replace("\\", "/")
					else:
						pathList[idx] = ""
						conflictList.append(name)
		for dirname in dirs:
			folderCnt += 1
	unexistFileList = map(lambda x:x[1], filter(lambda (bExist,name):not bExist, zip(existList,nameList)))
	unexistCnt = len(unexistFileList)
	print "引擎目录共有文件%d个，文件夹%d个"%(fileCnt,folderCnt)
	print "冲突文件%d个:"%len(conflictList), conflictList
	print "不存在文件%d个:"%unexistCnt, unexistFileList
	return pathList,conflictList

def read_file(filename, bStr):
	f = open(filename, "r")
	data = [line for line in f.readlines()]
	f.close()
	if bStr:
		return "".join(map(lambda s:s.rstrip()+"\n", data))
	else:
		return data

def write_file(filename, content):
	fd = open(filename,"w")
	fd.write(content)
	fd.close()

def print_list(lData):
	print "["
	for x in lData:
		print "\t", x
	print "]"



