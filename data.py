# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
import iorelated
import operate
from common import Singleton
from iorelated import print_list,write_file,Config


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
		self.__contents = []
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
			self.__contents.append(item)

	def build_namespace(self):
		for header in self.__headers:
			headername = header.headername()
			items = filter(lambda x:x.headername()==headername, self.__contents)
			#-----------------------------------------------------------------
			headerContent = header.detail()
			cc = operate.match_pair(headerContent, "NS_CC_BEGIN", "NS_CC_END")[1]
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

	def header_contents(self, headername):
		return filter(lambda x:x.headername()==headername, self.__contents)

	def build_element(self):
		self.build_class()
		self.build_enum()
		self.build_struct()

	def build_class(self):
		items = filter(lambda x:x.type()=="class", self.__contents)
		for item in items:
			name = item.name()
			namespace = item.namespace()
			detail = item.detail()
			header = item.headername()
			classObj = sClass(name, namespace, detail, header)
			self.__elements.append(classObj)

	def build_enum(self):
		items = filter(lambda x:x.type()=="enum", self.__contents)
		for item in items:
			name = item.name()
			namespace = item.namespace()
			detail = item.detail()
			enumObj = sEnum(name, namespace, detail)
			self.__elements.append(enumObj)

	def build_struct(self):
		pass

	def serialize_wrap(self):
		sMethodName = Config.getInstance().ModuleName()
		sDefaultOut1,sDefaultOut2 = iorelated.default_wrap_content()
		sClassOut = self.serialize_class()
		sEnumOut = self.serialize_enum()
		sStructOut = self.serialize_struct()
		out = ""
		out += sDefaultOut1
		out += "\n\n//暂时不需要封装构造函数\n"
		out += "BOOST_PYTHON_MODULE(%s)\n"%sMethodName
		out += "{\n"
		out += "\t// %s\n"%("-"*80)
		out += "\t// 枚举绑定\n"
		out += "\t// %s\n"%("-"*80)
		out += sEnumOut
		out += sStructOut
		out += sClassOut
		out += "}\n"
		out += sDefaultOut2
		return out

	def serialize_class(self):
		return ""

	def serialize_enum(self):
		lEnumOuts = map(lambda x:x.serialize(), filter(lambda x:isinstance(x,sEnum), self.__elements))
		out = "".join(lEnumOuts)
		return out

	def serialize_struct(self):
		return ""

	def generate(self):
		self.generate_wrap_file()

	def generate_wrap_file(self):
		out = self.serialize_wrap()
		sOutFileName = Config.getInstance().OutputDir()+"/py_cocos2dx_wrap_auto.cpp"
		write_file(sOutFileName, out)

	def in_listed_classes(self, class_name):
		pass

	def should_skip(self, class_name, method_name, verbose=False):
		pass








class sClass(object):
	def __init__(self, name, namespace, detail, header):
		self.__name = name
		self.__namespace = namespace
		self.__content = detail
		members = operate.Parser.getInstance().parse(detail, "extract_member", header)
		self.__members = self.build_member(members)

	def build_member(self, members):
		print "."*160
		iorelated.print_list(members)
		for memebr in members:
			member_data = operate.Parser.getInstance().parse(memebr, "parse_member")
		pass

	def serialize(self):
		pass

class sMember(object):
	def __init__(self):
		pass


	def serialize(self, bComment=False):
		pass

class sEnum(object):
	def __init__(self, name, namespace, detail):
		self.__name = name
		self.__namespace = namespace
		self.__content = detail
		self.__elements = self.parse_elem()

	def parse_elem(self):
		elements = filter(lambda x:x!="",
					map(lambda x:x.strip(), self.__content.strip()[1:-1].split(",")))
		elements = map(lambda x:x.partition("=")[0].strip(), elements)
		return elements

	def serialize(self):
		out = ""
		out += "\tenum_<%s%s>(\"%s\")\n"%(self.__namespace,self.__name,self.__name)
		for sElem in self.__elements:
			out += "\t\t.value(\"%s\", %s%s::%s)\n"%(sElem,self.__namespace,self.__name,sElem)
		out += "\t\t.export_values()\n"
		out += "\t\t;\n"
		return out

class sStruct(object):
	def __init__(self):
		pass



