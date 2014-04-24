__author__ = 'soujanya'

import sys,time
import dnet
from dpkt import bgp
from collections import defaultdict

ONE_DAY = 86400 #seconds

DELIMS = ( ('', ''),
           ('{', '}'),  # AS_SET
           ('', ''),    # AS_SEQUENCE
           ('(', ')'),  # AS_CONFED_SEQUENCE
           ('[', ']') ) # AS_CONFED_SET

def __init__():
  pass


class StableSetBuilder:
  def __init__(self):

    #self.parsed_list = list()
    self.stable_set = list()


  def path_to_str(self, path):
    string = ''
    for seg in path.segments:
        string += DELIMS[seg.type][0]
        for AS in seg.path:
            string += '%d ' % (AS)
        string = string[:-1]
        string += DELIMS[seg.type][1] + ' '

        '''
        Origin is given by the last AS in the AS_PATH "seg.len" provides the number of AS's in the AS_PATH
        Filter out only the last AS in the path
        '''
    return str(seg.path[seg.len-1])



  def test_for_stable_set(self, prefix_data, origin_as, prefix, announce_time):

    if (hasattr(prefix_data, "time")):
      if(announce_time - prefix_data.time >= ONE_DAY):
        print "Adding to stable set"
        self.stable_set[origin_as] = prefix
        prefix_data.marked = True

    else:
      prefix_data["time"] = announce_time
      prefix_data["marked"] = False


  def build(self, bgpdump):
    '''
    Given a BGPdump, constructs a stable set from the bgpdump.

    This function also returns a parsed form of the bgpdump that contains only
    prefix and time related data which is relevant for concurrent-hijack algorithm
    '''
    ORIG_AS = None

    as_set = defaultdict(dict)
    for mrt_h, bgp_h, bgp_m in bgpdump:

      ####Parse time at which announcements were made
      TIMEstr = time.strftime('%D %T', time.localtime())
      TIME = mrt_h.ts

      #######Print the origin from the AS Path attribute

      #print ("Attributes: %s" % bgp_m.update.attributes)
      for attr in bgp_m.update.attributes:
        if attr.type == bgp.AS_PATH:
          ORIG_AS = self.path_to_str(attr.as_path)
          #print ("ORIGIN AS: %s" % type(ORIG_AS))
          break

      #### If Bgp Update has no AS_PATH attribute, skip parsing this update
      if(ORIG_AS == None):
        print ("None AS")
        continue

      #### Initialize prefixes data
      if(hasattr(as_set, ORIG_AS)):
        prefixes_data = as_set[ORIG_AS]
      else:
        prefixes_data = dict()
        as_set[ORIG_AS] = prefixes_data


      ####Parse prefixes data
      for route in bgp_m.update.announced:
        #out('Announcement %d : %s/%d\n' % (i,dnet.ip_ntoa(route.prefix), route.len))
        PREFIX = dnet.ip_ntoa(route.prefix)

        #### Initialize prefix data
        if(hasattr(prefixes_data, PREFIX)):
          prefix_data = prefixes_data[PREFIX]
        else:
          prefix_data = dict()
          prefixes_data[PREFIX] = prefix_data

        #### If already in stable set skip parsing this prefix
        if(hasattr(prefix_data, "marked") and prefix_data.marked == True):
          continue

        self.test_for_stable_set(prefix_data, ORIG_AS, PREFIX, TIME)

      #parsed_list.append(as_set)

    return as_set




