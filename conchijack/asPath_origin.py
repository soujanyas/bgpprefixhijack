#!/usr/bin/env python
'''
Python module to capture and analyze data for concurrent prefix hijacks
'''

from optparse import OptionParser

from pybgpdump import BGPDump
from stable_set_builder import StableSetBuilder



def create_stable_set(dump):


  stable_set_builder = StableSetBuilder()
  orig = stable_set_builder.build(dump)
  print("Stable set entries are: \n%s" % stable_set_builder.stable_set)
  count = 0
  for k, v in orig.iteritems():
    #print k
    #print v
    count += 1
  print "Number of ASes in orig: %d" % count

def main():
    i=0
    ORIG_AS = "Return Value"
    PREFIX = "0"
    orig = dict()
    parsed_list = []
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', default='sample/updates.20011026.1322.bz2',help='read input from FILE', metavar='FILE')
    (options, args) = parser.parse_args()

    dump = BGPDump(options.input)

    create_stable_set(dump)



if __name__ == '__main__':
    main()
