'''
Python module to capture BGP hijack data from Argus
'''
import urllib.request
#import binascii
import re 

def get():
    s=urllib.request.urlopen("http://argus.csnet1.cs.tsinghua.edu.cn/api/alarms/100,123/").read()
    str=s.decode('ascii')
    dict = []
    n = 0
    #print(str)
    exp = re.compile(r'\{.+?\}')
    for line in exp.findall(str):
        res = exp.match(line).group().replace("{","").replace("}","").replace("\"", "")
        list = res.split(",")
        for pair in list:
            j = pair.split(":")  
            print ("count:%d %s" % (len(j), j))          
            dict.append()
        
        print (dict[n])
        n += 1
    #print("Len: %d" % len(res))
    
    #print(res) 
    return res

if __name__ == '__main__':
    #print("Hello") 
    get()

'''
Python module to capture BGP hijack data from Argus

import urllib.request
import binascii
import re
from collections import Counter 

def get():
    s=urllib.request.urlopen("http://argus.csnet1.cs.tsinghua.edu.cn/api/alarms/100,123/").read()
    str=s.decode('ascii')
    str.split(sep='[')
    str1=str.replace("[","").replace("]","").split(sep='},')
    dict=[]
    n = 0
    for i in str1:
        l=i.split(sep='{')
        r=[elem.strip().split(',') for elem in l]
        pairlist=[elem.strip().split(':') for elem in r[1]]
        for j in pairlist:
            ind_split = [elem.strip().split('"') for elem in j]
            #dict[ind_split[0][1]]=ind_split[1][1]
            print(ind_split[0][1])
            print(ind_split[1][1])
            #if(ind_split[0][1]):
                #dict[n][ind_split[0][1]] = ind_split[1][1]
        n += 1
    print (dict)    
    return str1

if __name__ == '__main__':
    #print("Hello") 
    get()
'''