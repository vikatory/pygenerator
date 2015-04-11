# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
import iorelated
import fileinfo
import operate
from iorelated import Config
from fileinfo import QFile

cocos_root = "E:/DATA_GIT/cocos2dx/project/CCGamePy/cocos2d/cocos"
cxxfilename = cocos_root + "/base/CCDirector.h"


def build_namespace(cursor, namespaces=[]):
    '''
    build the full namespace for a specific cursor
    '''
    if cursor:
        parent = cursor.semantic_parent
        if parent:
            if parent.kind == cindex.CursorKind.NAMESPACE or parent.kind == cindex.CursorKind.CLASS_DECL:
                namespaces.append(parent.displayname)
                build_namespace(parent, namespaces)

    return namespaces

def get_namespaced_name(declaration_cursor):
    ns_list = build_namespace(declaration_cursor, [])
    ns_list.reverse()
    ns = "::".join(ns_list)
    if len(ns) > 0:
        return ns + "::" + declaration_cursor.displayname
    return declaration_cursor.displayname


class Generator(object):
	def __init__(self, lCxxFileNames):
		self.__headers = lCxxFileNames

	def parse_headers(self):
		for header in self.__headers:
			prevName = config.PrevDir()+"/pre_"+fileinfo.QFile(header).basename()+".h"
			content = iorelated.read_file(header, True)
			content = operate.Parser().parse(content, "remove_comments")
			content = operate.Parser().parse(content, "remove_unused")
			content = operate.Parser().parse(content, "extract_class")
			iorelated.write_file(prevName, content)


			# print content
			pass
			# self._deep_iterate(tu.cursor)

	def _deep_iterate(self, cursor, depth=0):
		pass

	def in_listed_classes(self, class_name):
		pass

	def should_skip(self, class_name, method_name, verbose=False):
		pass





config = Config()
lCxxFileNames,conflictList = iorelated.detect_walk_search(config.EngineRoot(), config.FileName())
iorelated.print_list(lCxxFileNames)
# @Note:对不同文件夹有同名文件的情况不做处理，自行处理，输出到conflictList提示一下
generator = Generator(lCxxFileNames)
generator.parse_headers()

#print "================================================================="


