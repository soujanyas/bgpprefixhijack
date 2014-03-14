#!/bin/env/python

'''
Python module to capture BGP hijack data from Argus
'''

import urllib.request
import re


class ArgusCapture:

  def get(self, url):
    '''
    Invokes HTTP GET method on the given URL to retrieve BGP updates from Argus
    '''
    s = urllib.request.urlopen(url).read()
    str = s.decode('ascii')
    dlist = list()
    n = 0

    #Get all the entries corresponding to one BGP message
    exp = re.compile(r'\{.+?\}')
    for line in exp.findall(str):
        res = exp.match(line).group().replace("{","").replace("}","").replace("\"", "")
        dictobj  = dict()
        for pair in res.split(","):
            j = pair.split(":")
            if(len(j) != 2):
              assert False, "Format error, key value pair does not exist"
            dictobj[j[0].strip()] = j[1].strip()

        dlist.append(dictobj)
        n += 1
    return dlist

if __name__ == '__main__':
    argus_capture = ArgusCapture()
    res = argus_capture.get("http://argus.csnet1.cs.tsinghua.edu.cn/api/alarms/100,123/")
    print (res)
    for index, item in enumerate(res):
      print ("%d : time:%s" % (index, item["timestamp"]))