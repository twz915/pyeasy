'''
read sqlite3 database
2013-10-31 16:46:55

TODO: read database include sqlite3, MySQL, PostgreSQL

'''

import sqlite3

class SqliteReader:
	'''
	Usage: 
		sqliteReader(DB).excute(command)
		sqliteReader(DB).select(tablename,columns)
	'''
	def __init__(self,DBname):
		with sqlite3.connect(DBname) as self.conn:
			self.cur = self.conn.cursor()

	def execute(self,command):
		self.cur.execute(command)
		self.conn.commit()
		result = self.cur.fetchall()
		print repr(result)
		
		return result

	def select(self,tableName,*args):
		command="select %s from %s" %(",".join(args),tableName) # select * is no problem
		self.execute(command)
		
	def insert(self,tableName,columns,values):
		command = 'insert into %s (%s) values("%s")' %(tableName,columns,values)
		self.execute(command)

	def __finally__(self):# __del__  ?
		self.conn.commit()
		self.cur.close()
		self.conn.close()
		print "cur.close() conn.close()"


if __name__ == "__main__":
	dbf = SqliteReader("db.sqlite3")
	dbf.insert('book_author','name','1234567890')
	dbf.execute('select * from book_author')

