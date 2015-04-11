# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os
import ConfigParser
from common import Singleton
from fileinfo import QFile


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


class Config(Singleton):
	__hasParsered = False
	def __init__(self):
		if not self.__hasParsered:
			self.parse()

	def parse(self):
		config = ConfigParser.ConfigParser()
		config.read("config.ini")
		#-----------------------------------------------------------------------
		self.__EngineRoot = config.get("search_path", "EngineRoot")
		self.__ProjectRoot = config.get("search_path", "ProjectRoot")
		self.__FileName = config.get("search_path", "FileName")
		self.__IgnoreInherit = config.get("search_path", "IgnoreInherit")
		self.__OutputDir = config.get("search_path", "OutputDir")
		self.__PrevDir = config.get("search_path", "PrevDir")
		self.__ModuleName = config.get("search_path", "ModuleName")
		#-----------------------------------------------------------------------
		self.__FileName = self.__FileName.strip()[1:-1].split(",")
		self.__FileName = map(lambda s:s.strip(), self.__FileName)
		self.__IgnoreInherit = self.__IgnoreInherit.strip()[1:-1].split(",")
		#-----------------------------------------------------------------------

	def EngineRoot(self):
		return self.__EngineRoot

	def ProjectRoot(self):
		return self.__ProjectRoot

	def FileName(self):
		return self.__FileName

	def IgnoreInherit(self):
		return self.__IgnoreInherit

	def OutputDir(self):
		return self.__OutputDir

	def PrevDir(self):
		sPrevDir = self.__ProjectRoot+"/"+self.__PrevDir
		return sPrevDir

	def ModuleName(self):
		return self.__ModuleName



