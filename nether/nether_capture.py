#!/usr/bin/python3
__author__ = 'soujanya'

FILE = 0
DATE = 1
PREFIX = 2
AS_PATH = 3
CONTACT = 4
SCORE = 5
BLAME = 6

#Reference: https://docs.python.org/3/library/html.parser.html
#           http://strftime.org/


from html.parser import HTMLParser
import time
import urllib.request
import random

def __init__():
  pass

class NetherCapture(HTMLParser):
  def __init__(self):
    #196.43.197.0%2F24
    #11259+6453+17400

    HTMLParser.__init__(self)
    self.time_format = "%Y-%m-%d"
    self.nether_time_format = "%Y-%m-%d %H:%M:%S.%f"
    self.nether_url = "http://puck.nether.net/bgp/leakinfo.cgi?search=do&search_prefix=$prefix&search_aspath=$as_path&search_asn=&recent=2000"

  def handle_starttag(self, tag, attrs):
    if(tag == "td"):
      self.td_read = True
    #print("Encountered tag : %s", tag)

  def check_if_in_range(self, start_time, end_time, data):
    start = time.mktime(time.strptime(start_time, self.time_format))
    end = time.mktime(time.strptime(end_time, self.time_format))
    event_time = time.mktime(time.strptime(data, self.nether_time_format))
    if(start < event_time and event_time < end):
      return True

  def handle_data(self, data):
    if(self.td_read):
            #Ignore first entry the says 'TIME'
      if (self.counter % 7 == DATE and not (self.counter == 1)):

        if (self.check_if_in_range(self.start_time, self.end_time, data)):
          #We don't get any data right now
          self.events_in_range += 1

      self.counter += 1
      self.td_read = False

###############################################################################
#Handle url fetching of data

  def make_url(self, a_res):
    url = self.nether_url
    asn = ""
    prefix = ""
    if(len(a_res) > 0):
      prefix = a_res['prefix'].replace("/","%2F")
      asn = a_res['bad_path_segment'].replace(" ", "+")
      asn = a_res['origin'] + asn
    url = url.replace("$as_path", asn)
    url = url.replace("$prefix", prefix)
    return url

  def parse_nether_results(self, data_stream, from_time, to_time):
    '''
    Parses nether data and returns number of entries that fall in range
    '''
    #print("calling with ds: %s" % data_stream)
    self.td_read = False
    self.counter  = 0
    self.events_in_range = 0
    self.start_time = from_time
    self.end_time = to_time
    self.feed(data_stream)
    #Feed internally calls handle_starttag which marks td tags and handle_data
    # which checks whether data is td and extracts the data
    self.close()
    return self.events_in_range


  def get_nether_data(self, from_time, to_time, a_res):
    url = self.make_url(a_res)
    print("NETHER: Constructed URL: %s" % url)
    n_data = urllib.request.urlopen(url).read().decode('utf-8')
    return self.parse_nether_results(n_data, from_time, to_time)

  def count_nether_anam(self, from_time, to_time):
    a_res = {}
    #data = self.get_nether_data(from_time, to_time, a_res)
    ##testing
    data = random.randrange(2000, 6000)
    return data

  def has_nether_anam(self, from_time, to_time, a_res):
    return self.get_nether_data(from_time, to_time, a_res) > 0

################################################################################
# Test case for nether

def test_nether_url_parsing():
  sample_ds = '''
<!-- saved from url=(0136)http://puck.nether.net/bgp/leakinfo.cgi?search=do&search_prefix=196.43.197.0%2F24&search_aspath=11259+6453+17400&search_asn=&recent=2000 -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><style type="text/css"></style></head><body><div id="StayFocusd-infobar" style="display: none; top: 0px;">
    <img src="chrome-extension://laankejkbhbdhmipfmgcngdelahlfoji/common/img/eye_19x19_red.png">
    <span id="StayFocusd-infobar-msg"></span>
    <span id="StayFocusd-infobar-links">
        <a href="http://puck.nether.net/bgp/leakinfo.cgi?search=do&search_prefix=196.43.197.0%2F24&search_aspath=11259+6453+17400&search_asn=&recent=2000#" id="StayFocusd-infobar-never-show">hide forever</a>&nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="http://puck.nether.net/bgp/leakinfo.cgi?search=do&search_prefix=196.43.197.0%2F24&search_aspath=11259+6453+17400&search_asn=&recent=2000#" id="StayFocusd-infobar-hide">hide once</a>
    </span>
</div>BGP Routing Leak Detection System<style type="text/css">
<!--
TD{font-family: Arial; font-size: 10pt;}
--->
</style>Routing Leak Detection System<p>
We use a simple technique where we process RIB and BGP UPDATE snapshots to find either persistent or Transient routing leaks that exist.  We have a series of "BIG" Networks that should not show up in a sequence.  Example: UUNet (701) does not buy from Sprint (1239) to get to Globalcrossing (3549).  This means if we see an as-path with all three of these in the path, it is flagged and stored.  We do exclude a few business relationships in our processing.  (Examples are that Telia 1299 is known to buy transit from UUNet).  For a list of the <a href="http://puck.nether.net/bgp/leaks-majornet.txt">major networks</a> we match, follow the link.</p><p>Attempting to show the most recent 2000 detected by our system.  We use two data sources, one a BGP feed located on puck, the second is processing the BGP Updates from the <a href="http://www.routeviews.org/">Route Views</a> project.  The source column either show puck, which is just a RIB snapshot or the file name from <a href="http://www.routeviews.org/">Route Views</a> that we processed.</p><p> We also attempt to determine the asn responsible for accepting the routing leak.  That is shown in the Contact column.  We are using a  modified version of the zebra-dump-parser.pl script.  Copies are available upon request.</p><p>Networks that want to get automated notices when they are involved in one of these leaks, or responsible for a leak should contact Jared Mauch directly.  He can add you for now and we may add an automated system soon enough.</p><p>General statistics are available from the system via the following <a href="http://puck.nether.net/bgp/stats.html">link</a>.  We started collecting all the available data from route-views during 2007-09-06 and later, so this is why there is an increase.</p><p>Known major events: 2007-08-25 - AS3561 leaked a large number of peer routes to other peers<br></p><p></p><form method="GET" action="http://puck.nether.net/bgp/leakinfo.cgi">Search the data:
<br><input type="HIDDEN" name="search" value="do">
Prefix: <input name="search_prefix" type="TEXT" value="196.43.197.0/24"> eg: 127.0.0/8 or 35.42.1.0/24 are valid -- do not forget a netmask :) <br>
AS_PATH: <input name="search_aspath" type="TEXT" value="11259 6453 17400"> eg: "1668_3561"<br>
Contact ASN: <input name="search_asn" type="TEXT" value=""> eg: 6461<br>
Number of Recent: <input name="recent" value="2000"><br>
<input type="submit" value="Lookup">
<input type="RESET" value="Clear">
 </form>
<p>Time is in US/Eastern time currently.
</p><p><a href="http://puck.nether.net/bgp/leakinfo.cgi">Search this data</a><table border="1">
<tbody><tr><td>Source</td><td>Time</td><td>Prefix</td><td>AS_PATH</td><td>Contact?</td><td>Score</td><td>blame_asn</td></tr>
<tr><td>updates.20140329.2230.bz2</td><td>2014-03-29 22:50:05.265371</td><td>196.43.197.0/24</td><td> 11686 19782 4323 701 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140329.2230.bz2</td><td>2014-03-29 22:50:05.246693</td><td>196.43.197.0/24</td><td> 2497 701 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140329.2230.bz2</td><td>2014-03-29 22:50:05.228007</td><td>196.43.197.0/24</td><td> 11686 3356 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140329.2230.bz2</td><td>2014-03-29 22:50:05.204222</td><td>196.43.197.0/24</td><td> 2497 2914 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140329.2230.bz2</td><td>2014-03-29 22:50:05.159946</td><td>196.43.197.0/24</td><td> 3356 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140307.1815.bz2</td><td>2014-03-07 18:40:05.939525</td><td>196.43.197.0/24</td><td> 11686 19782 4323 701 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr>
<tr><td>updates.20140307.1815.bz2</td><td>2014-03-07 18:40:05.91653</td><td>196.43.197.0/24</td><td> 11686 3356 174 8657 36881 11259 6453 17400 36917 37267 </td><td>174</td><td>3</td><td>8657</td></tr
</tbody></table></p></body></html>
    '''

  nether = NetherCapture()
  n_results = nether.parse_nether_results(sample_ds, "2014-03-20", "2014-03-30")
  assert n_results == 5

def test_nether_url():
  a_res = dict()
  a_res['origin'] = ""
  a_res['bad_path_segment'] = "11259 6453 17400"
  a_res['prefix'] = "196.43.197.0/24"
  nether = NetherCapture()
  n_results = nether.get_nether_data("2014-03-20", "2014-03-30", a_res)
  assert n_results == 5
  assert nether.has_nether_anam("2014-03-20", "2014-03-30", a_res) == True

if __name__ == "__main__":
  test_nether_url_parsing()
  test_nether_url()




