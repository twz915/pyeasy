#!/usr/bin/python
#coding:utf-8

import os
import shutil


class FileHandle:
	'''
	import filehandle
	files_list = filehandle.FileHandle().listAllFiles(path)
	filehandle.FileHandle().replaceFileContent(path,primary,replace))

	'''
	def __init__(self,*args):
		if len(args)==1:
			if args[0].strip()=="safeoff":self.mode="safeoff"
			else:self.mode="safeon"
		else:
			self.mode="safeon"
		self.allfileslist = []

	def copyfile(self,pri,tar):	
		shutil.copyfile(pri,tar)

	def movefile(self,pri,tar):
		shutil.move(pri,tar)

	def deletefile(self,path):
		os.remove(path)

	def getExtension(self,path):
		L = os.path.split(path)[1].split(".")
		return L[len(L)-1]

	def getFolder(self,path):
		return os.path.split(path)[0]

	def getFilename(self,path):
		return os.path.split(path)[1]

	def listAllFiles(self,path):
		'''
		List = os.listdir(path)
		for f in List:
			tp = path + f
			if os.path.isfile(tp):self.allfileslist.append(tp)
			elif os.path.isdir(tp):self.listAllFiles(tp+"/")# '/' very important!!!

		return self.allfileslist
		
		'''
		List = []
		[List.extend(map(lambda f:os.path.join(r,f), fs) for r,ds,fs in os.walk(path))]

		return List



	def headAdd(self,path,content,checkrepeat="off"):
		f = open(path)
		primaryContent = f.read()
		f.close()
		if checkrepeat == 'on' and primaryContent.strip().find(content.strip()) == 0:
			print "Repeat! passed! File: ",path
		else:
			backupPath = path + ".backup." + self.getExtension(path)
			if self.mode == "safeon":
				self.copyfile(path,backupPath)#copy file
			try:
				f = open(path,"w")
				f.write(content + os.linesep*2 +primaryContent)
				f.close()
			except:
				try:self.copyfile(backupPath,path)
				except:pass#no backup if users safeoff
				print "Failed:",path



	def replaceFileContent(self,path,primary,replace):
		f = open(path)
		primaryContent = f.read()
		f.close()

		Content = primaryContent.replace(primary,replace)

		backupPath = path + ".backup." + self.getExtension(path)
		if self.mode == "safeon":
			self.copyfile(path,backupPath)#copy file

		try:
			f = open(path,"w")
			f.write(Content)
			f.close()
		except:
			try:self.copyfile(backupPath,path)#copy file back
			except:pass#no backup if users safeoff
			print "Failed:",path

		print self.runningTips


if __name__ == "__main__":
	#print Folder().listAllFiles("/home/tu/try/")
	FileHandle().headAdd("/home/tu/views.py","import settings"+os.linesep+"rootpath = settings.RootPath")
	FileHandle().replaceFileContent("/home/tu/views.py",'"/home/tu/','rootpath + "')
	FileHandle().replaceFileContent("/home/tu/views.py","'/home/tu/","rootpath + '")


#end