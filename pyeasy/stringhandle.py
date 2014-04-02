'''
22/09/2013 tuweizhong
String Handle
'''
import re

class StringHandle:
	'''
	# Usage:
	#   from pyeasy.stringhandle import StringHandle as sh
	#	sh(string).findAll(subString)
	#	sh(string).find(subString,postion)
	# for examples:
	list = sh("students,boy").findAll("a")# return a list "[0,7]" of all the positions of "a" in string "students,boy"
	
	sh("students,boy").find("s",-1)#return 7, the last "s" in string "students,boy"
	sh("students,boy").find("s",2)#return the second "s" in string "students,boy"

	sh("<a>It works</a>").between("<a>","</a>") #return "It works"
	'''

	def __init__(self,string):
		self.str=str(string)
			

	def findAll(self,findStr):
		findList=[]
		start=0
		while True:
			index=self.str.find(findStr,start)
			if index == -1:
				break
			start = index + 1
			findList.append(index)
		return findList

	def find(self,string,pos=1):
		findList = self.findAll(string)
		if pos < 0:
			pos = len(findList)+pos
		elif pos > 0:
			pos -= 1
		else:
			return None
		try:return findList[pos]
		except:return None

	def between(self,start,end):# StringHandle("<a>It works</a>").between("<a>","</a>") #return "It works"
		begin_pos=self.find(start)+len(start)
		endPosList=self.findAll(end)
		for end_pos in endPosList:
			if end_pos > begin_pos:
				break
		return self.str[begin_pos:end_pos]
		
	def between2(self,start,end):
		pattern = start + '(.*?)' + end
		reg = re.compile(pattern)
		return reg.findall(self.str)
		

	def remove(self,start,end):
		begin_pos=self.find(start)
		endPosList=self.findAll(end)
		for end_pos in endPosList:
			if end_pos > begin_pos:
				end_pos += len(end)
				break
		return self.str[:begin_pos] + self.str[end_pos:]
	
	def remove2(self,start,end,include=True):# if include, remove start and end together
		pattern = start + '(.*?)' + end
		reg = re.compile(pattern)
		if include:
			return reg.sub('',self.str)
		else:
			return reg.sub(start+end,self.str)
	
	def left(self,string):
		pos = self.str.find(string)
		if pos >=-1:
			return self.str[0:pos]
		else:return None

	def right(self,string):
		pos = self.str.find(string)
		if pos >=-1:
			return self.str[pos+len(string):]
		else:return None




if __name__ == "__main__":
	print StringHandle('SmallMolecule227361:[<string title="smiles">[O-]S([O-])=O</string> <string title="systematicName">trioxosulfate(2-)</string> ]').between2('<string title="smiles">',"</string>")

	print StringHandle('SmallMolecule227361:[<string title="smiles">[O-]S([O-])=O</string> <string title="systematicName">trioxosulfate(2-)</string> ]').remove('<string title="systematicName">',"</string>")

	print StringHandle("abcdefgabcabcaabcdaa").findAll("a")

#end
