# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
from common import Singleton
from iorelated import print_list
from operate import match_pair


class sContent(object):
	def __init__(self, type, headername, breaf, detail):
		self.__type = type
		self.__headername = headername
		self.__breaf = breaf
		self.__detail = detail
		self.__name = self.build_name(type, breaf)
		self.__namespace = ""

	def type(self):
		return self.__type

	def name(self):
		return self.__name

	def headername(self):
		return self.__headername

	def breaf(self):
		return self.__breaf

	def detail(self):
		return self.__detail

	def namespace(self):
		return self.__namespace

	def build_name(self, type, breaf):
		if type == "class":
			name = filter(lambda x:x.strip()!="", breaf.partition(":")[0].split(" "))[-1]
		elif type == "enum":
			name = filter(lambda x:x.strip()!="", breaf.split(" "))[-1]
		elif type == "struct":
			name = breaf
		else:
			name = ""
		return name

	def build_namespace(self, namespace):
		self.__namespace += namespace + "::"


class Elements(Singleton):
	def __init__(self):
		self.__headers = []
		self.__elements = []

	def addHeaders(self, header, content, stype):
		if stype == "header":
			if header in map(lambda x:x.headername(), self.__headers):
				raise "%s已添加"%header
			item = sContent("header", header, header, content)
			if item not in self.__headers:
				self.__headers.append(item)

	def extend(self, header, lData, stype):
		for breaf, detail in lData:
			item = sContent(stype, header, breaf, detail)
			self.__elements.append(item)

	def build_namespace(self):
		for header in self.__headers:
			headername = header.headername()
			items = filter(lambda x:x.headername()==headername, self.__elements)
			#-----------------------------------------------------------------
			headerContent = header.detail()
			cc = match_pair(headerContent, "NS_CC_BEGIN", "NS_CC_END")[1]
			for item in items:
				if cc.find(item.detail())!=-1:
					item.build_namespace("cocos2d")
			#-----------------------------------------------------------------
			items.sort(key=lambda x:[len(x.detail())])
			count = len(items)
			for i in xrange(count):
				for j in xrange(count-1, i, -1):
					item, item_n = items[i], items[j]
					if item_n.detail().find(item.detail())!=-1:
						item.build_namespace(item_n.name())
			# print_list(map(lambda x:(x.name(),x.namespace()), items))

	def build_element(self):
		self.build_class()
		self.build_enum()
		self.build_struct()

	def build_class(self):
		pass

	def build_enum(self):
		items = filter(lambda x:x.type()=="enum", self.__elements)
		for item in items:
			name = item.name()
			namespace = item.namespace()
			detail = item.detail()
			EnumObj = sEnum(name, namespace, detail)
		print items

	def build_struct(self):
		pass



class sClass(object):
	def __init__(self):
		pass

class sEnum(object):
	def __init__(self, name, namespace, detail):
		self.__name = name
		self.__namespace = namespace
		self.__content = detail
		self.parse_elem()

	def parse_elem(self):
		print self.__content
		pass

	def serialize(self):
		pass

class sStruct(object):
	def __init__(self):
		pass




