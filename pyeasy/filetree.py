#!/usr/bin/env python
#coding:utf-8

import os

def fileTree(path, count=0):
    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        fileName = os.path.basename(path)
        print '    ' * count + '|-- ' + fileName 
    elif os.path.isdir(path):
        print '    ' * count + '|-- ' + path 
        pathList = os.listdir(path)
        for eachPath in pathList:
            fileTree(os.path.join(path,eachPath),count+1)
 
if __name__ == '__main__':
	fileTree('/home/tu/pyeasy')
