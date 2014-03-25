'''
Read excel file easyer
@author: Weizhong Tu 2013-09-19 08:59:20 
modified @ 2013.12.28 23:14
'''

import os
import re

from pyeasy.stringhandle import StringHandle

from pyExcelerator import parse_xls,Workbook


class OpenExcel:
	'''
	#Usage: 
	from pyeasy.excel import OpenExcel
	f = OpenExcel(path) #default sheet(1) you can use 'f = OpenExcel(path).sheet(2)

	########### read data ###########
	f.read()                               #return all data

	f.read(1) or read("1")                 # return a list of line data (horizontal)
	f.read("A")                            # return a list of column data (vertical)
	f.read('A7') or read('24A')            # return a string of special data!
	f.read("A","1")
	#you can also use read("A",1) read(1,"A") or read("1","A")
	
	########### read sheet name ###########
	OpenExcel(path).sheet(2).readSheetName()   # return a string of sheet2 name
	f.readAllsheetsName()                      # return a list of all sheets names

	########### getposition ###########
	f.getPosition("tuweizhong")#default completeMatch=False,stripOn=False #find a string position in excel
	#for examples:
	OpenExcel("/home/tu/tu.xls").getPosition("3D")#default completeMatch=False,stripOn=False
	OpenExcel("/home/tu/tu.xls").getPosition("3D",completeMatch=True,stripOn=True) or ("3D",1,1)
	'''

	def __init__(self,path,mode="r"):
		self.path = path
		self.mode = mode
		if mode=="r":
			if os.path.exists(path):
				try:
					self.data = parse_xls(path)
					self.sheets = self.data[0]
				except IndexError:
					self.sheets = ""
					print "Can't find sheet %d"%sheet
				except:
					self.sheets = ""
					print "Unknown Error!"
			else:
				print "Can't find %s" %path
		elif mode=="w":
			self.newexcel = Workbook()
			self.ws = self.newexcel.add_sheet('sheet1')

		elif mode=="a":#add to excel
			pass

	def __toNum(self,args):
		if len(args)==1:
			return (ord(args.upper())-ord("A"))
		if len(args)==2:
			return ((ord(args[0].upper())-ord("A") + 1)*26 +  (ord(args[1].upper())-ord("A"))) #AA means 26

	def __hasChar(self,args):
		if re.compile('[a-zA-Z]').search(str(args)):
			return True
		return False

	def __hasNum(self,args):
		if re.compile('[0-9]').search(str(args)):
			return True
		return False
	


	'''
	#=================================
	#      A     B     C     D     E  
	#  1 (0,0) (0,1) (0,2) (0,3) (0,4)
	#  2 (1,0) (1,1) (1,2) (1,3) (1,4)
	#  3 (2,0) (2,1) (2,2) (2,3) (2,4)
	#=================================
	# (row,col)
	'''

	def _convert(self,args):#convert '(1,1)' to 'B2' and 'B2' to '(1,1)' auto-recongnize
		if args.find(",") > -1:
			b,a=args.replace("(","").replace(")","").split(",")
			a=chr(int(a)+65)#chr(65) is "A" and ord("A") is 65
			b=str(int(b)+1)
			return a+b
		else:
			a=str(int(args[1:2])-1)               # D1-->(0,3)   1-->0
			b=str(ord(args[0:1].upper())-65)      # D1-->(0,3)   D-->3       ord("D") is 68
			return "("+a+","+b+")"

	def readSheetName(self):
		return self.sheets[0]

	def readAllSheetsName(self):
		sL = len(self.data)
		sheetNameList = []

		for i in range(sL):
			sheetNameList.append(sC[i][0])
		return sheetNameList

	def getPosition(self,string,completeMatch=False,stripOn=False):#edit to find all positions
		tmp=repr(self.sheets)
		posList = []#positions list
		pList = StringHandle(tmp).findAll(string)#if can't find return vacant list []

		for p in pList:
			list1=StringHandle(tmp[:p]).findAll("(")# >>> a[:43]
			begin=list1[len(list1)-1]
			list2=StringHandle(tmp[:p]).findAll(":")# "[(u'sheetname1', {(0, 1): u'1B', (1, 2): u'"
			end=list2[len(list2)-1]
			posList.append(self._convert(tmp[begin:end]))

		if completeMatch:#remove incomplete match!
			for i in posList:
				readString = self.read(i)
				if stripOn:
					readString = readString.strip()

				if readString != string:
					posList.remove(i)
		return sorted(posList)

	def sheet(self,sheet_num):
		self.sheets = self.data[sheet_num-1]
		
	def read(self,*args):
		if self.sheets == "":
			return#stop here if read failed

		elif len(args) == 0: # read() return all data
			return self.data

		elif len(args) == 1:# read('A') or read('10') or read('A3')
			#1. judge read a line or a position
			args = str(args[0])
			if self.__hasChar(args) and self.__hasNum(args):# contains char and num ,such as "A5"
				# read('A3')
				_char = ''.join(re.compile('[a-zA-Z]').findall(args))
				_num = ''.join(re.compile('[0-9]').findall(args))
				return self.read(_char,_num)

			# read('A') or read('10') #bugs here! use read('A',3)
			tmpList = []

			if self.__hasNum(args):
				for i in self.sheets[1]:
					if (i[0] == int(args)-1):
						tmpList.append(self.sheets[1].get(i))
			else:
				for i in self.sheets[1]:
					if (i[1] == self.__toNum(args)):
						tmpList.append(self.sheets[1].get(i))

			return tmpList

		elif len(args) == 2:#read a given position, such as read("A",10)
			if self.__hasNum(args[1]):
				b = self.__toNum(args[0])
				a = int(args[1])-1
			else:
				a = int(args[0])-1
				b = int(self.__toNum(args[1]))

			return self.sheets[1].get((a,b))

	def write(self,position,content):#write("A2","ecoli")
		a,b = self._convert(position).replace("(","").replace(")","").split(",")
		self.ws.write(int(a),int(b),str(content))
		
	def save(self):
		if self.mode == "w":
			self.newexcel.save(self.path)
		else:print "OpenExcel mode is not 'w',OpenExcel(path,'w')"


if __name__ == "__main__":
	p = OpenExcel("/home/tu/try.xls","w")
	p.write("A2","A2")
	p.write("D3","D3")
	p.save()

#The end
