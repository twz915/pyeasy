'''
Tue 12 Nov 2013 10:10:58 CST
@author tuweizhong
'''

import json

class OpenJson(object):
	"""
	from jsonhandle import OpenJson

	OpenJson(file).read()
	OpenJson(file).write(content)

	"""
	
	def __init__(self,path):
		self.path=path
	
	def read(self):# read json file
		try:
			f=open(self.path)
			data = json.load(f)
			f.close()
		except:
			f = open(self.path)
			data = f.read()
			f.close()
			# convert read data to a dict
			data=eval(data)

		return data
	
	def write(self,content):# write a dict to file
		f = open(self.path,"w")
		json.dump(content, f, indent=4)
		f.close()




