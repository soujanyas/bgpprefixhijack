'''
Python module to capture and analyze data for concurrent prefix hijacks
'''

from pybgpdump import BGPDump

filename = "sample/updates.20011026.1322.bz2"

if __name__ == "__main__":
    dump = BGPDump(filename);
    count = 0
    pkt =  dump.next()
    try:
        while pkt:
            count += 1
            pkt = dump.next()
    except StopIteration:
        print "count = %d" % count
