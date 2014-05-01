#!/usr/bin/python3

import urllib.request



def __init__():
    pass

class CyclopsCapture:
    
    def __init__(self):
        self.trans_url = "http://cyclops.cs.ucla.edu/transientPrefixOrigins/?action=query&di=$from_time&de=$to_time&asn=$asn&prfx="

    def has_transient_results(self, from_time, to_time, a_res):
      ####Construct the required URL
      transient_url = self.trans_url.replace("$from_time", from_time)
      transient_url = transient_url.replace("$to_time", to_time)
      seg = a_res['bad_path_segment'].replace(" ", "+")
      asn = a_res['origin'] + seg
      transient_url = transient_url.replace("$asn", asn)

      print("Searching for ASN: %s" % asn)
      print("Constructed URL: %s" % transient_url)

      cyclops_res = urllib.request.urlopen(transient_url).read()
      res = cyclops_res.decode('utf-8')

      #print(cyclops_res)
      if("Total of" in res):
        return True
      else:
        return False
       #http://cyclops.cs.ucla.edu/transientPrefixOrigins/?action=query&di=2014-04-24&de=2014-05-01&asn=15835+51833&prfx=

def test_transient():
    cycplos_capture = CyclopsCapture()
    a_res = dict()
    a_res['origin'] = ""
    a_res['bad_path_segment'] = "15835 51833"
    assert cycplos_capture.has_transient_results("2014-04-23", "2014-04-30",a_res) == True
    a_res['bad_path_segment'] = "1234"
    assert cycplos_capture.has_transient_results("2014-04-23", "2014-04-30",a_res) == False



if __name__ == '__main__':
    test_transient()