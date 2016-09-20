# -*- coding: utf-8 -*-
import sys
import yaml
import fileinput
import time

def replaceV(dataMapStatic,block):
    for key,val in dataMapStatic.iteritems():
        rkey = "{{"+str(key)+"}}"
        for k,v in block.iteritems():
            if v is not None:
                print v + " ....bbbb..."
                print key
                if key in v: print key+" "+"in"+" "+v
                new_v = v.replace(rkey,str(val))
                print new_v + " .....aaaaa..."
                block[k]=new_v

def add(operationVal):
    print "<<<<<<<.................This is in add....................>>>>>>"
    filename = str(operationVal.get('filename'))
    prefixes = str(operationVal.get('prefixes'))
    add = str(operationVal.get('add'))
    suffixes = str(operationVal.get('suffixes'))

    print "filename: " + str(filename)
    print "prefixes: " + str(prefixes)
    print "add: " + str(add)
    print "suffixes: " + str(suffixes)

    processing_foo1s = False
    count = 0
    for line in fileinput.input(filename.strip(), inplace=1):
        if prefixes == 'None' and count ==0:
            print add
            count +=1

        if prefixes in line:
            processing_foo1s = True
        else:
            if processing_foo1s:
                    print add
            processing_foo1s = False
        print line.strip()



def update(operationVal):
    print "<<<<.....................This is in update..............>>>>"
    filename = str(operationVal.get('filename'))
    prefixes = str(operationVal.get('prefixes'))
    src = str(operationVal.get('src'))
    dst = str(operationVal.get('dst'))
    suffixes = str(operationVal.get('suffixes'))

    print "filename: " + str(filename)
    print "prefixes: " + str(prefixes)
    print "src: " + src
    print "dst: " + str(dst)
    print "suffixes: " + str(suffixes)

    for line in fileinput.input(filename.strip(), inplace=1):
        if src in line:
            print dst
        else:
            print line.strip()
    fileinput.close()

def delete(operationVal):
    print " <<<<...........This is in delete..........>>>>>"
    filename = str(operationVal.get('filename'))
    prefixes = operationVal.get('prefixes')
    compare = str(operationVal.get('del'))
    suffixes = operationVal.get('suffixes')

    print "filename: " + str(filename)
    print "prefixes: " + str(prefixes)
    print "delete: " + str(compare)
    print "suffixes: " + str(suffixes)
    for line in fileinput.input(filename, inplace=1):
        if compare in line:
            print ""
        else:
            print line.strip()

def getSubDict(dataMapStatic):
    subDict = dict()
    for key,val in dataMapStatic.iteritems():
        rkey = "{{"+str(key)+"}}"
        subDict[rkey]=val

    return subDict

def getSubFileList(dataMapOps):
    subFileList = list()

    for module in dataMapOps['UPDATE']:
        for fileDict in module['conf']:
            subFileList.append(fileDict['filename'])

    return subFileList

def subFile(filename,src,dst):
    print " inside the subFile method......>>>>>J"
    print "filename: " + str(filename)
    print "  ..."
    try:
        for line in fileinput.input(filename.strip(), inplace=1):
            tmpline = str(line)
            if src in line:
                index=tmpline.index(src)
                print tmpline[:index]+str(dst)+tmpline[index+len(src):]
            else:
                print line.strip()

        fileinput.close()
    except Exception as e:
        print e
        fileinput.close()
        return



def substitu(dataMapOps,dataMapStatic):
    subFileList = getSubFileList(dataMapOps)
    subDict = getSubDict(dataMapStatic)

    print subFileList
    print subDict

    for file in subFileList:
        for src,dst in subDict.iteritems():
            subFile(file,src,dst)
def initiate(opconfi,staconf):

    dataMapStatic = None
    if (staconf != None):
        f1 = open(staconf)
        dataMapStatic = yaml.safe_load(f1)
        f1.close()

    f1 = open(opconfi)
    dataMapOps = yaml.safe_load(f1)
    f1.close()

    if (staconf != None):
        for module in dataMapOps['UPDATE']:
            for fileDict in module['conf']:
                replaceV(dataMapStatic,fileDict)

    if(staconf != None):
        substitu(dataMapOps,dataMapStatic)
        return

    for key,val in dataMapOps.iteritems():
        for module in val:
            for block in module['modify']:
                if key == "ADD":
                    add(block)
                if key == "UPDATE":
                    update(block)
                if key == "DEL":
                    delete(block)


if __name__=="__main__":
    opconfi,staconf = (None,None)
    if len(sys.argv)==3:
        opconfi,staconf=(sys.argv[1],sys.argv[2])
    else:
        opconfi = sys.argv[1]

    initiate(opconfi,staconf)

