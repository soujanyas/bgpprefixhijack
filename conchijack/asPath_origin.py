#!i/usr/bin/env python
'''
Python module to capture and analyze data for concurrent prefix hijacks
'''

from optparse import OptionParser
from dpkt import bgp
from pybgpdump import BGPDump
import sys,time
import dnet
from collections import defaultdict

data = defaultdict(list)
orig = defaultdict(dict)
d = list()

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
	Origin is given by the last AS in the AS_PATH "seg.len" provides the number of AS's in the AS_PATH
	Filter out only the last AS in the path
	''' 
        #print('Origin : %s' % (seg.path[seg.len-1]))
	return seg.path[seg.len-1]
def main():
    i=0
    AS = "Return Value"
    PREFIX = "0"
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', default='sample/updates.20011026.1322.bz2',help='read input from FILE', metavar='FILE')
    (options, args) = parser.parse_args()
    out = sys.stdout.write
    dump = BGPDump(options.input)
    for mrt_h, bgp_h, bgp_m in dump:
	'''
	Print the origin from the AS Path attribute
	'''
        for attr in bgp_m.update.attributes:
           if attr.type == bgp.AS_PATH:
                AS=path_to_str(attr.as_path)
	''' 
	To print the BGP announce messages
	'''
	i=1
	TIME = time.strftime('%D %T', time.localtime(mrt_h.ts))
	#out('TIME: %s\n' %(time.strftime('%D %T', time.localtime(mrt_h.ts))))
	#out('TIME: %s\n' %(TIME))
	
        for route in bgp_m.update.announced:
		PREFIX = dnet.ip_ntoa(route.prefix)
	        #out('Announcement %d : %s/%d\n' % (i,dnet.ip_ntoa(route.prefix), route.len))
		i=i+1
		data[PREFIX].append(TIME)
	#if AS in orig:
	#	orig[AS].append(data)
	#else:
	orig[AS]=data
	#print (AS)
	d.append(AS)
	#print (' ')
    '''for key, value in orig.iteritems() :
	if(key==3112):
    		print key, value
	if(key==6221):
    		print key, value
	if(key==21702):
    		print key, value
	print(' ')'''
    #print (' ')
    #print(orig[3112])
    #print (' ')
    #print(orig[6221])
    #print (' ')
    #print(orig[21702])
    #print (' ')
    dest = list(set(d))
    dest.sort()
    print dest
    #print(len(dest))
if __name__ == '__main__':
    main()
