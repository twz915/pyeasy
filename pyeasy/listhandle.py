'''
@author: tuweizhong
name: listHandle
2013-10-28 14:12:28 
'''
class ListHandle:

	def __init__(self,List):
		self.l=List

	def indexAll(self,f):
		findList=[]
		start=0
		while True:
			try:index=self.l.index(f,start) # if can't find,ValueError
			except:break
			start = index + 1
			findList.append(index)
		return findList

	def removeRepeat(self):
		L=list(set(self.l))
		return L
			


if __name__=="__main__":

	l=[1,"2",2,"2",3,2,2,3,5,2]
	print ListHandle(l).indexAll(2)
	

