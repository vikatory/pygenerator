# -*- coding:utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015年3月30日

@author: ming
'''
import re
from common import Singleton
import iorelated


class Parser(Singleton):
	def __init__(self):
		pass

	def parse(self, content, sParseType):
		if sParseType == "remove_comments":
			result = PRemoveComments(content).result()
			return result
		if sParseType == "remove_unused":
			result = PRemoveUnused(content).result()
			return result
		if sParseType == "extract_class":  # 先解析类，因为类能包含其他类型
			result = PExtractClass(content).result()
			return result
		if sParseType == "extract_enum":
			result = PExtractEnum(content).result()
			return result
		if sParseType == "extract_struct":
			result = PExtractStruct(content).result()
			return result
		if sParseType == "extract_func":
			pass
		if sParseType == "extract_member":
			pass
		return None


class PRemoveComments(object):
	''' 移除注释 '''
	def __init__(self, content):
		self.__content = content

	def remove_comments(self):
		content = self.__content
		content = content.replace("\t", "    ")
		#-----------------------------------------------------------------------
		lPatts = [
			("/\*[\s\S]*?\*/", ""),  # 移除/* */
			("//.*\n", "\n"),  # 一般头文件里的字符串里没有//，这里先不考虑字符串里的//
			("\n +\n", "\n"),  # 缩减空白行，\n空白\n——>\n
			]
		#-----------------------------------------------------------------------
		for sPatt, sTar in lPatts:
			content = search_and_replace_all(content, sPatt, sTar)
		return content

	def result(self):
		return self.remove_comments()

class PRemoveUnused(object):
	''' 移除不需要的内容 '''
	def __init__(self, content):
		self.__content = content

	def remove_unused(self):
		content = self.__content
		content = content.strip().replace("\n\n","\n")
		#-----------------------------------------------------------------------
		content = search_and_replace_all(content, "#[ ]+", "#")  # 删除#后的空格
		#-----------------------------------------------------------------------
		beg_patt = re.compile("(?P<cnt>\A#ifndef.+\n#define.+\n)")
		end_patt = re.compile("(?P<cnt>\n#endif.*\Z)")
		beg_mo = beg_patt.search(content)
		end_mo = end_patt.search(content)
		if beg_mo and end_mo:
			sBeg = beg_mo.group("cnt")
			sEnd = end_mo.group("cnt")
			content = content.replace(sBeg, "", 1)
			content = content.rpartition(sEnd)[0]+"\n"
		#-----------------------------------------------------------------------
		content = search_and_replace_all(content, "#include.+\n", "", True)
		content = search_and_replace_all(content, "\n.*class\s[^\n\{]*;", "\n", True)  # 剔除声明的类/友元类，没有定义体
		content = search_and_replace_all(content, "typedef\s[^\{\};]*;", "", True)  # 剔除类型的定义，如typedef void* id;
		content = search_and_replace_all(content, "using\s[^\{\}\(\);]*;", "", True)
		content = search_and_replace_all(content, "#if.+\n\s*#endif\n", "", True)
		content = search_and_replace_all(content, "\n\n", "\n", True)
		#-----------------------------------------------------------------------
		return content

	def result(self):
		return self.remove_unused()


class PExtractClass(object):
	''' 提取类的内容 '''
	def __init__(self, content):
		self.__content = content

	def extract_class(self):
		content = " "+self.__content+" "  # 兼容匹配
		patt = re.compile("(?P<match>[\s;\{\}](enum)?\s*class\s[^\{\}]+\{)")
		matchs = patt.findall(content)
		matchs = map(lambda x:x[1:].strip() if x[0] in ["{","}",";"] else x,
				map(lambda (a,b):a[:-1].strip(), matchs))
		matchs = filter(lambda x:not x.startswith("enum"), matchs)  # 类声明列表
		result = map(lambda x:(x, match_pair(content, "{","}", content.find(x)+len(x))[1]), matchs)
		return result

	def result(self):
		return self.extract_class()


class PExtractEnum(object):
	''' 提取枚举的内容 '''
	def __init__(self, content):
		self.__content = content

	def extract_enum(self):  # 只提取第一层的类，嵌套的类用稍后处理
		content = " "+self.__content+" "  # 兼容匹配
		patt = re.compile("(?P<match>[\s;\{\}]enum\s+(class)?\s*[^\{\}]+\{)")
		# 没名字的enum没有提取
		matchs1 = patt.findall(content)
		matchs1 = map(lambda x:x[1:].strip() if x[0] in ["{","}",";"] else x,
				map(lambda (a,b):a[:-1].strip(), matchs1))
		result = map(lambda x:(x, match_pair(content, "{","}", content.find(x)+len(x))[1]), matchs1)
		#-----------------------------------------------------------------------
		patt = re.compile("(?P<match>[\s;\{\}]typedef\s+enum\s+\{[^\{\}]+\}[^;]+;)")
		matchs2 = patt.findall(content)
		matchs2 = map(lambda x:x[1:].strip() if x[0] in ["{","}",";"] else x,
				map(lambda a:a[:-1].strip(), matchs2))
		result += map(lambda x:(x[x.rfind("}")+1:].strip(), match_pair(x, "{","}")[1]), matchs2)
		#-----------------------------------------------------------------------
		return result

	def result(self):
		return self.extract_enum()


class PExtractStruct(object):
	''' 提取结构体的内容 '''
	def __init__(self, content):
		self.__content = content

	def extract_struct(self):  # 只提取第一层的类，嵌套的类用稍后处理
		content = " "+self.__content+" "  # 兼容匹配
		patt = re.compile("(?P<match>[\s;\{\}](typedef)?\s*struct\s[^\{\}]+\{)")
		matchs1 = patt.findall(content)
		matchs1 = map(lambda x:x[1:].strip() if x[0] in ["{","}",";"] else x,
				map(lambda (a,b):a[:-1].strip(), matchs1))
		result = map(lambda x:(x, match_pair(content, "{","}", content.find(x)+len(x))[1]), matchs1)
		lTmp = []
		for s, detail in result:
			if s.startswith("typedef"):
				name = match_pair(content,"}",";",content.find(detail)+len(detail)-1)[1]
				name = name[1:-1].strip()
			else:
				name = filter(lambda m: m.strip()!="", s.split(" "))[-1]
			lTmp.append((name, detail))
		result = lTmp
		#-----------------------------------------------------------------------
		return result

	def result(self):
		return self.extract_struct()












def search_and_replace_all(content, sPatt, sTar, bRstrip=False):
	patt = re.compile("(?P<match>%s)"%sPatt)
	mo = patt.search(content)
	while mo:
		match = mo.group("match")
		content = content.replace(match, sTar, 1)
		mo = patt.search(content)
	result = content
	if bRstrip:
		result = search_and_replace_all(result, " +\n", "\n")  # 删除\n前的空格
	return result

def search_and_replace_all_test(content, sPatt, sTar):
	ocontent = content
	patt = re.compile("(?P<match>%s)"%sPatt)
	mo = patt.search(content)
	while mo:
		match = mo.group("match")
		print match
		content = content.replace(match, sTar, 1)
		mo = patt.search(content)
	return ocontent

def match_pair(content, head, tail, pos=0):  # pos为匹配的开始位置
	''' 匹配成对的模式，例如括号，if,endif等 '''
	#-------------------------------------------------------------------------
	iLeftCnt, iRightCnt, iLeft, iRight, iHeadLen, iTailLen = 0, 0, 0, 0, len(head), len(tail)
	content = content[pos:]
	i, contentLen = 0, len(content)
	while i < contentLen:  # 考虑这种特殊配对(if, ifend)(ifend, if), 待优化
		sHeadTry = content[i:i+iHeadLen]
		sTailTry = content[i:i+iTailLen]
		if iLeftCnt == 0:
			if sHeadTry == head:
				iLeftCnt += 1
				iLeft = i
				i += iHeadLen
			else:
				i += 1
		else:
			if sHeadTry == head and sTailTry == tail:
				if iHeadLen >= iTailLen:
					iLeftCnt += 1
					i += iHeadLen
				else:
					iRightCnt += 1
					i += iTailLen
			elif sHeadTry == head and sTailTry != tail:
				iLeftCnt += 1
				i += iHeadLen
			elif sHeadTry != head and sTailTry == tail:
				iRightCnt += 1
				i += iTailLen
			else:
				i += 1
		if iLeftCnt == iRightCnt and iLeftCnt != 0:
			iRight = i
			return content[:iLeft], content[iLeft:iRight], content[iRight:]
	return content, "", ""  # 找不到匹配的返回值，content已被裁剪了



