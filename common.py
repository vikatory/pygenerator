# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import os
import re
import sys


class Singleton(object):
	"A python style singleton"
	def __new__(cls, *args, **kw):  # 用这种方法，__init__被反复的调用了
		if not hasattr(cls, "_instance"):
			org = super(Singleton, cls)
			cls._instance = org.__new__(cls, *args, **kw)
		return cls._instance

	@classmethod
	def getInstance(cls, *args, **kw):
		if not hasattr(cls, "_instance"):
			return cls(*args, **kw)
		return cls._instance













