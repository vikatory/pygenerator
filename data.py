# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os
import re
import sys


class sContent(object):
	def __init__(self, type, breaf, detail, namespace):
		self.__type = type
		self.__breaf = breaf
		self.__detail = detail
		self.__namespace = namespace

	def type(self):
		return self.__type

	def breaf(self):
		return self.__breaf

	def detail(self):
		return self.__detail

	def namespace(self):
		return self.__namespace






