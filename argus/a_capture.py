#!/bin/env/python

'''
Python module to capture BGP hijack data from Argus
'''

import urllib.request
import re
import time
#/home/soujanya/opt/Python-3.3.5/python a_capture.py
NUM_ALARMS = 1000
time_format = "%Y-%m-%d %H:%M:%S"

class ArgusCapture:

  def __init__(self):
    self.url = "http://argus.csnet1.cs.tsinghua.edu.cn/api/"

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

  def get_all_results(self, url):
    i = 0
    results = list()
    while i < NUM_ALARMS:
      res = self.get(url + "%d,%d" %(i, i + 99))
      results.extend(res)
      i += 100
      #print ("%d -> %d" % (i, i+100))
    return results

      #for index, item in enumerate(res):
      #  print ("%d : time:%s" % (index, item["timestamp"]))

  def in_range(self, start_date, end_date, timestamp):
    start = time.mktime(time.strptime(start_date, time_format))
    end = time.mktime(time.strptime(end_date, time_format))
    #print("%s -> %s : %s" %(start, end, timestamp))
    if float(timestamp) > start and float(timestamp) < end:
      return True
    return False

  def get_entries_in_range(self, start, end, url):
    all_entries = self.get_all_results(url)
    entries_in_range = []
    print("Alarms/Anomalies in range:\n")
    for index,entry in enumerate(all_entries):
      if(self.in_range(start, end, entry["timestamp"])):
        print ("## %s" % entry)
        entries_in_range.append(entry)
    return entries_in_range

  def get_alarms_in_range(self, start, end):
    print("Looking for alarms in range: %s -> %s.." %(start, end))
    alarm_url = self.url + "alarms/"
    return self.get_entries_in_range(start, end, alarm_url)

  def get_anomalies_in_range(self, start, end):
    print("Looking for anomalies in range: %s -> %s..\n" %(start, end))
    anomaly_url = self.url + "anomalous/"
    return self.get_entries_in_range(start, end, anomaly_url)

#####TEST CASES

def test_in_range():
  start = "2010-10-01 01:01:01"
  end = "2012-10-01 01:01:01"
  timestamp = ("%s") % time.mktime(time.strptime("2011-04-01 01:01:01",time_format))
  assert ArgusCapture().in_range(start, end, timestamp)
  timestamp = ("%s") % time.mktime(time.strptime("2014-04-30 01:01:01",time_format))
  assert (not ArgusCapture().in_range(start, end, timestamp))



if __name__ == '__main__':
    argus_capture = ArgusCapture()
    argus_capture.get_alarms_in_range("2012-04-01 01:01:01", "2012-04-30 01:01:01")
    argus_capture.get_anomalies_in_range("2013-12-01 01:01:01", "2014-01-01 01:01:01")
    test_in_range()
    #for index, item in enumerate(res):
    #  print ("%d : time:%s" % (index, item["timestamp"]))


