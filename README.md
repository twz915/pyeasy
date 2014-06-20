pyeasy
==============

To make python programing easier
----------------------


1. read excel
------

    from pyeasy import OpenExcel
    f = OpenExcel('test.xls')
    f.read() # read all
    f.read('A') # read 'A' row
    f.read(1) # f.read('1'), read '1' column
    f.read('A5') # read 'A5' position


2. web visitor
-------------

    from pyeasy import webvisitor
    webvisitor.get(url,data)
    webvisitor.post(url,data)


3. print file tree
--------------------

    from pyeasy.filetree import fileTree
    fileTree('/home/tu') #print the directory file tree
