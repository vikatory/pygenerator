# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os
import ConfigParser
import time
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
		print "-----------------------------"
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
		return self.__ProjectRoot+"/"+self.__OutputDir

	def PrevDir(self):
		sPrevDir = self.__ProjectRoot+"/"+self.__PrevDir
		return sPrevDir

	def ModuleName(self):
		return self.__ModuleName


def default_wrap_content():
	stime = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
	sMethodName = Config.getInstance().ModuleName()
	sDefaultOut1 = """
// --------------------------------------------------------------------------------
// @Created     : %s
// @Desc        : 程序自动封装
// --------------------------------------------------------------------------------

#include "py_cocos2dx_Wrap.h"
#include "py_cocos2dx_OutMember.h"
#include "py_cocos2dx_WrapClass.h"
#include "cocos2d.h"
#include <boost/python.hpp>
#include <boost/utility.hpp>
#include <memory>
using namespace boost::python;

#ifdef HELD_BY_AUTO_PTR
# define HELD_PTR(X) , std::auto_ptr< X >
#else
# define HELD_PTR(X)
#endif 
"""%stime
	#-----------------------------------------------------------------------
	sDefaultOut2 = """
void registerPymodule_%s()
{
	// 注册模块到解释器中
	if (PyImport_AppendInittab(const_cast<char*>("%s"),
#if PY_VERSION_HEX >= 0x03000000 
		PyInit_%s
#else 
		init%s
#endif 
		) == -1)
		throw std::runtime_error("把common作为内建模块加载到解释器失败");
}
//#include "module_tail.cpp"
"""%(sMethodName,sMethodName,sMethodName,sMethodName)
	#-----------------------------------------------------------------------
	return sDefaultOut1.lstrip(), sDefaultOut2

