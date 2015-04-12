# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
from common import Singleton


class sContent(object):
	def __init__(self, type, headername, breaf, detail):
		self.__type = type
		self.__headername = headername
		self.__breaf = breaf
		self.__detail = detail
		# self.__namespace = namespace

	def type(self):
		return self.__type

	def headername(self):
		self.__headername

	def breaf(self):
		return self.__breaf

	def detail(self):
		return self.__detail

	def namespace(self):
		return self.__namespace


class Elements(Singleton):
	def __init__(self):
		self.__headers = []
		self.__elements = []

	def addHeaders(self, header, content, stype):
		if stype == "header":
			if header in map(lambda x:x.headername(), self.__headers):
				raise "%s已添加"%header
			item = sContent("header", header, header, content)
			self.__headers.append(item)

	def extend(self, header, lData, stype):
		for breaf, detail in lData:
			item = sContent(stype, header, breaf, detail)
			self.__elements.append(item)





