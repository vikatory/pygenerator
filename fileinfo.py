# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os
import re
import sys

class QFile(object):
	def __init__(self, fullfilename): # @Parm: 完整的绝对路径
		self.__filename = self.format_name(fullfilename)

	def format_name(self, filename):
		filename = filename.replace("\\\\","/")
		filename = filename.replace("\\","/")
		filename = filename.replace("//","/")
		return filename

	def basename(self):
		name = self.__filename.rpartition("/")[2]
		name = name.rpartition(".")[0]
		return name

	def fullname(self):
		return self.__filename







