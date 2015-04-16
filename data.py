# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
import iorelated
from common import Singleton
from iorelated import print_list,write_file,Config
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

	def serialize_wrap(self):
		sDefaultOut1,sDefaultOut2 = iorelated.default_wrap_content()
		sClassOut = self.serialize_class()
		sEnumOut = self.serialize_enum()
		sStructOut = self.serialize_struct()
		out = sDefaultOut1+sClassOut+sEnumOut+sStructOut+sDefaultOut2
		return out

	def serialize_class(self):
		return ""

	def serialize_enum(self):
		return ""

	def serialize_struct(self):
		return ""

	def generate(self):
		self.generate_wrap_file()

	def generate_wrap_file(self):
		out = self.serialize_wrap()
		sOutFileName = Config.getInstance().OutputDir()+"/py_cocos2dx_wrap_auto.cpp"
		print sOutFileName
		write_file(sOutFileName, out)

	def in_listed_classes(self, class_name):
		pass

	def should_skip(self, class_name, method_name, verbose=False):
		pass








class sClass(object):
	def __init__(self):
		pass

class sEnum(object):
	def __init__(self, name, namespace, detail):
		self.__name = name
		self.__namespace = namespace
		self.__content = detail
		self.__elements = self.parse_elem()

	def parse_elem(self):
		print self.__content
		elements = filter(lambda x:x!="",
					map(lambda x:x.strip(), self.__content.strip()[1:-1].split(",")))
		elements = map(lambda x:x.partition("=")[0].strip(), elements)
		return elements

	def serialize(self):
		pass

class sStruct(object):
	def __init__(self):
		pass




