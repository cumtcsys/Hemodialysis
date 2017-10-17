# -*- coding: utf-8 -*-
def writeListToFile(filename,listcontents):
    fo = open(filename,'a')
    string = ""
    for item in listcontents:
        string= string +" "+ item
    fo.writelines(string+"\n")
    fo.close()
writeListToFile(r"deep/result.txt","sssssssssss")