'''
Python module to capture BGP hijack data from Argus
'''
import urllib.request
import binascii
from collections import Counter 

def get():
    s=urllib.request.urlopen("http://argus.csnet1.cs.tsinghua.edu.cn/api/alarms/100,123/").read()
    str=s.decode('ascii')
    str1=str.split(sep=':')
    print(str)
    print("\n")
    for i in str1:
        print(i)
        #print(Counter(str1[i]))
    return s

if __name__ == '__main__':
    print("Hello") 
    print(get())