#coding=utf8
 
import zipfile
import optparse
from threading import Thread
 
def extractFile(zFile,password):
    try:
        zFile.extractall(pwd = password.encode(encoding="utf-8"))
        print("[+] Found password " + password + "\n")
    except Exception as e:
        print(str(e))#如果不需要输出不成功的结果，直接改成pass
 
def main():
    parse = optparse.OptionParser("useage%prog " + "-f <zipfile> -d <dictionary>")
    parse.add_option("-f",dest="zname",type="string",help="specify zip file")
    parse.add_option("-d",dest="dname",type="string",help="specify dictionary file")
    (options,args) = parse.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parse.usage)
    else:
        zname = options.zname
        dname = options.dname
        zFile = zipfile.ZipFile(zname)
        passFile = open(dname)
        for line in passFile.readlines():
            password = line.strip("\n")
            t = Thread(target = extractFile,args=(zFile,password))
            t.start()
 
if __name__ == "__main__":
    main()
