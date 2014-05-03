#!/usr/bin/python3

__author__ = 'soujanya'
import urllib.request
import re



def __init__():
    pass

class CyclopsCapture:
    
    def __init__(self):
        self.trans_url = "http://cyclops.cs.ucla.edu/transientPrefixOrigins/?action=query&di=$from_time&de=$to_time&asn=$asn&prfx="
        self.depeering_url = "http://cyclops.cs.ucla.edu/anomalousDepeerings/?action=query&di=$from_time&de=$to_time&asn=$asn&tp="
        self.bogus_asn_url = "http://cyclops.cs.ucla.edu/bogusASNs/?action=query&di=$from_time&de=$to_time&asn=$asn&asn_bogus="
        self.bogon_prefix_url = "http://cyclops.cs.ucla.edu/bogonPrefixes/?action=query&di=$from_time&de=$to_time&asn=$asn&prfx="
        self.prefix_len_url = "http://cyclops.cs.ucla.edu/longShortPrefixes/?action=query&di=$from_time&de=$to_time&asn=$asn&prfx="


    def make_url(self, from_time, to_time, url, a_res):
      '''
      Generic method to construct URL of the required type
      '''
      url = url.replace("$from_time", from_time)
      url = url.replace("$to_time", to_time)
      asn = ""
      if(len(a_res) > 0):
        seg = a_res['bad_path_segment'].replace(" ", "+")
        asn = a_res['origin'] + seg

      url = url.replace("$asn", asn)
      print("CYCLOPS: Searching for ASN: %s" % asn)
      print("CYCLOPS: Constructed URL: %s" % url)

      return url

    def get_count_results(self, cyclops_res):
      res = cyclops_res.decode('utf-8')
      grp = re.search(r'Total of (?P<num>.*) row', res)
      if grp is None:
        return 0
      grpd = grp.groupdict()
      return int(grpd['num'])

    def make_request(self, from_time, to_time, a_res, url_template):
      url = self.make_url(from_time, to_time, url_template, a_res)
      cyclops_res = urllib.request.urlopen(url).read()
      return self.get_count_results(cyclops_res)

    def has_transient_prefix_anam(self, from_time, to_time, a_res):
      '''
      Method that checks whether passed argus result has transient prefixes
      '''
      return self.make_request(from_time, to_time, a_res, self.trans_url) > 0

    def has_depeering_anam(self, from_time, to_time, a_res):
      return self.make_request(from_time, to_time, a_res, self.depeering_url) > 0

    def has_bogus_asn_anam(self, from_time, to_time, a_res):
      return self.make_request(from_time, to_time, a_res, self.bogus_asn_url) > 0

    def has_bogon_prefix_anam(self, from_time, to_time, a_res):
      return self.make_request(from_time, to_time, a_res, self.bogon_prefix_url) > 0

    def has_prefix_len_anam(self, from_time, to_time, a_res):
      return self.make_request(from_time, to_time, a_res, self.prefix_len_url) > 0


    def count_transient_prefix_anam(self, from_time, to_time):
      '''
      Method that checks whether passed argus result has transient prefixes
      '''
      a_res = {}
      return self.make_request(from_time, to_time, a_res, self.trans_url)

    def count_depeering_anam(self, from_time, to_time):
      a_res = {}
      return self.make_request(from_time, to_time, a_res, self.depeering_url)

    def count_bogus_asn_anam(self, from_time, to_time):
      a_res = {}
      return self.make_request(from_time, to_time, a_res, self.bogus_asn_url)

    def count_bogon_prefix_anam(self, from_time, to_time):
      a_res = {}
      return self.make_request(from_time, to_time, a_res, self.bogon_prefix_url)

    def count_prefix_len_anam(self, from_time, to_time):
      a_res = {}
      return self.make_request(from_time, to_time, a_res, self.prefix_len_url)
       #http://cyclops.cs.ucla.edu/transientPrefixOrigins/?action=query&di=2014-04-24&de=2014-05-01&asn=15835+51833&prfx=

def test_transient():
    cycplos_capture = CyclopsCapture()
    a_res = dict()
    a_res['origin'] = ""
    a_res['bad_path_segment'] = "15835 51833"
    assert cycplos_capture.count_transient_prefix_anam("2014-04-23", "2014-04-30",a_res) == 8
    assert cycplos_capture.has_transient_prefix_anam("2014-04-23", "2014-04-30",a_res) == True
    a_res['bad_path_segment'] = "1234"
    assert cycplos_capture.count_transient_prefix_anam("2014-04-23", "2014-04-30",a_res) == 0
    assert cycplos_capture.has_transient_prefix_anam("2014-04-23", "2014-04-30",a_res) == False

if __name__ == '__main__':
    test_transient()