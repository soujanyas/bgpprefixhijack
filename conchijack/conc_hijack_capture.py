#!/usr/bin/python3

__author__ = 'soujanya'

import urllib.request
import re

class ConcHijackCapture():
  def __init__(self):
    self.trans_url = "http://cyclops.cs.ucla.edu/transientPrefixOrigins/?action=query&di=$from_time&de=$to_time&asn=&tp=&pp=$pn&sort=lifetime"

  def make_url(self, page_num, from_time, to_time):
    url = self.trans_url
    url = url.replace("$from_time", from_time)
    url = url.replace("$to_time", to_time)
    url = url.replace("$pn", str(page_num))
    return url

  def count_num_pages(self, data_stream):
    page = re.search(r'\(page (?P<pnum>.*)/(?P<total>.*)\)', data_stream)
    if(page is not None):
      n_pages = page.groupdict()["total"]
      print ("Number of pages: %d", int(n_pages))
      return n_pages
    else:
      return 0

  def count_num_entries(self, url):
    page_data = urllib.request.urlopen(url).read().decode('utf-8')
    return page_data.count("0 days")
    #One day in cyclops is technically 2 days
    #self.c_one_day += page_data.count("1 days")

  def count_conc_hijack_anam(self, from_time, to_time):
    url = self.make_url(0, from_time, to_time)
    ch_results = urllib.request.urlopen(url).read().decode('utf-8')
    num_pages = self.count_num_pages(ch_results)
    count = 0
    for i in range(int(num_pages)):
      url = self.make_url(i, from_time, to_time)
      print ("Constructed URL is: %s" % url)
      c_zero_day = self.count_num_entries(url)
      print("count returned: %d" % c_zero_day)
      count += c_zero_day
      if(c_zero_day == 0):
        print("Breaking at : %d" % i)
        break

    return count

def test_conc_hijack():
  conc_hijack_capture = ConcHijackCapture()
  assert conc_hijack_capture.count_conc_hijack_anam("2014-04-26","2014-05-03") == 7714


if __name__ == "__main__":
  test_conc_hijack()

