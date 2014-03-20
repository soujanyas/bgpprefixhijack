 #!i/usr/bin/env python
'''
Python module to capture and analyze data for concurrent prefix hijacks
'''

from optparse import OptionParser
from dpkt import bgp
from pybgpdump import BGPDump
import sys,time
import dnet

DELIMS = ( ('', ''),
           ('{', '}'),  # AS_SET
           ('', ''),    # AS_SEQUENCE
           ('(', ')'),  # AS_CONFED_SEQUENCE
           ('[', ']') ) # AS_CONFED_SET

def path_to_str(path):
    str = ''
    for seg in path.segments:
        str += DELIMS[seg.type][0]
        for AS in seg.path:
            str += '%d ' % (AS)
        str = str[:-1]
        str += DELIMS[seg.type][1] + ' '
	'''  
	Origin is given by the last AS in the AS_PATH
	"seg.len" provides the number of AS's in the AS_PATH
	Filter out only the last AS in the path
	'''
        print(seg.path[seg.len-1])

def main():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', default='sample/updates.20011026.1322.bz2',
                      help='read input from FILE', metavar='FILE')
    (options, args) = parser.parse_args()
    out = sys.stdout.write
    dump = BGPDump(options.input)
    for mrt_h, bgp_h, bgp_m in dump:
	'''
	Print the origin from the AS Path attribute
	'''
        for attr in bgp_m.update.attributes:
           if attr.type == bgp.AS_PATH:
                path_to_str(attr.as_path)
	''' 
	To print the BGP announce messages
	'''
        for route in bgp_m.update.announced:
	        out('%s/%d\n' % (dnet.ip_ntoa(route.prefix), route.len))

if __name__ == '__main__':
    main()
