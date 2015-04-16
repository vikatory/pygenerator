# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import iorelated
import fileinfo
import operate
import data
from iorelated import Config
from fileinfo import QFile


class Generator(object):
	def __init__(self, lCxxFileNames):
		self.__headers = lCxxFileNames

	def parse_headers(self):
		for header in self.__headers:
			parser = operate.Parser.getInstance()
			elements = data.Elements.getInstance()
			prevName = config.PrevDir()+"/pre_"+QFile(header).basename()+".h"
			headername = QFile(header).basename()
			content = iorelated.read_file(header, True)
			content = parser.parse(content, "remove_comments")
			content = parser.parse(content, "remove_unused")
			elements.addHeaders(headername, content, "header")
			result = parser.parse(content, "extract_class")
			elements.extend(headername, result, "class")
			result = parser.parse(content, "extract_enum")
			elements.extend(headername, result, "enum")
			result = parser.parse(content, "extract_struct")
			elements.extend(headername, result, "struct")
			iorelated.write_file(prevName, content)
		elements.build_namespace()
		elements.build_element()
		elements.generate()




config = Config.getInstance()
lCxxFileNames,conflictList = iorelated.detect_walk_search(config.EngineRoot(), config.FileName())
iorelated.print_list(lCxxFileNames)
# @Note:对不同文件夹有同名文件的情况不做处理，自行处理，输出到conflictList提示一下
generator = Generator(lCxxFileNames)
generator.parse_headers()



